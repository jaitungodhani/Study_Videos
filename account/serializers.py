from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_data"] = {
            'id': self.user.id,
            'email': self.user.email,
            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None,
            'role':self.user.role
        }
        return data
    
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        exclude = ('is_staff','is_superuser','groups','user_permissions','last_login')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_role(self, obj):
        return obj.role

class UserCreateSerializer(serializers.ModelSerializer):
    USER_ROLE_CHOICES = (
        'Faculty', _('Faculty'),
        'Student', _('Student')
    )
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required = True)
    
    class Meta:
        model = User
        exclude = ('is_staff','is_superuser','groups','user_permissions','last_login','is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
        exclude = ('is_staff','is_superuser','groups','user_permissions','last_login','is_active', 'password')

    def to_representation(self, instance):
        return UserSerializer(instance).data