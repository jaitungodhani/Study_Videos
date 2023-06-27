import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from payment.models import StripeCustomer
from study_videos.celery import send_mail

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        sub_obj = StripeCustomer.objects.filter(user=self.user).first()
        print(sub_obj)
        if sub_obj:
            sub_status = stripe.Subscription.retrieve(
                sub_obj.stripeSubscriptionId,
            )

            if sub_status.status == "active":
                if self.user.is_facultyuser:
                    self.user.groups.set("")
                    self.user.groups.add("Subscribed Faculty")

                if self.user.is_studentuser:
                    self.user.groups.set("")
                    self.user.groups.add("Subscribed Student")

            else:
                if self.user.is_subscribedfacultyuser:
                    self.user.groups.set("")
                    self.user.groups.add("Faculty")

                if self.user.is_subscribedstudentuser:
                    self.user.groups.set("")
                    self.user.groups.add("Student")

        data["user_data"] = {
            "id": self.user.id,
            "email": self.user.email,
            "profile_picture": self.user.profile_picture.url if self.user.profile_picture else None,
            "role": self.user.role,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ("is_staff", "is_superuser", "groups", "user_permissions", "last_login")
        extra_kwargs = {"password": {"write_only": True}}

    def get_role(self, obj):
        return obj.role


class UserCreateSerializer(serializers.ModelSerializer):
    USER_ROLE_CHOICES = ("Faculty", _("Faculty"), "Student", _("Student"))
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True)

    class Meta:
        model = User
        exclude = ("is_staff", "is_superuser", "groups", "user_permissions", "last_login", "is_active")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        self.password = validated_data.pop("password")
        user = super(UserCreateSerializer, self).create(validated_data)
        group = get_object_or_404(Group, name__iexact=role)
        user.groups.add(group)
        user.set_password(self.password)
        user.save()
        return user

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_staff", "is_superuser", "groups", "user_permissions", "last_login", "is_active", "password")

    def to_representation(self, instance):
        return UserSerializer(instance).data


class ActivateAccountEmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        self.email = attrs["email"]
        try:
            self.user = User.objects.get(email=self.email)
            if self.user.is_active:
                raise serializers.ValidationError("Account Is already active")
        except User.DoesNotExist:
            raise serializers.ValidationError("Email is Wrong, Please check !!!!")
        return super(ActivateAccountEmailSendSerializer, self).validate(attrs)

    def send_mail(self):
        link = f"http://127.0.0.1:8000/api/userusermanager/account-activate/?user_id={self.email}&confirmation_token={default_token_generator.make_token(self.user)}"

        subject = "Activate Account of Study Videos App"
        message = get_template("mail_body.html").render({"link": link, "user": UserSerializer(self.user).data})
        send_mail.apply_async(
            args=[subject, message, self.email],
        )


class ActivateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)

            if self.user.is_active:
                raise Exception("Account Already Activated!!!")

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
        if self.user is None:
            raise Exception("User Not Found")
        return True

    def validate_token(self, value):
        if not default_token_generator.check_token(self.user, value):
            raise Exception("Token is invalid or expired. Please request another confirmation email by signing in.")
        return True

    def set_active(self):
        self.user.is_active = True
        self.user.save()


class ForgotpasswordEmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        self.email = attrs["email"]
        try:
            self.user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No Active account found with this email")
        return super(ForgotpasswordEmailSendSerializer, self).validate(attrs)

    def send_mail(self):
        link = f"http://127.0.0.1:8000/api/userusermanager/account-activate/?user_id={self.email}&confirmation_token={default_token_generator.make_token(self.user)}"

        subject = "Change Password for your Study Videos App account"
        message = get_template("forgot_password.html").render({"link": link, "user": UserSerializer(self.user).data})
        send_mail.apply_async(
            args=[subject, message, self.email],
        )


class ForgotpasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
        if self.user is None:
            raise Exception("User Not Found")
        return True

    def validate_token(self, value):
        if not default_token_generator.check_token(self.user, value):
            raise Exception("Token is invalid or expired. Please request another confirmation email by signing in.")
        return True

    def set_password(self, password):
        self.user.set_password(password)
        self.user.save()


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        self.password = attrs["old_password"]
        self.new_password = attrs["new_password"]
        self.request = self.context.get("request")

        if not self.request.user.check_password(self.password):
            raise serializers.ValidationError("Password is Not Valid!!!")

        return super(ResetPasswordSerializer, self).validate(attrs)

    def set_password(self):

        self.request.user.set_password(self.new_password)
        self.request.user.save()
