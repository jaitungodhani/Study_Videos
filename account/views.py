from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.permissions import (
    IsAdmin,
    IsFaculty,
    IsStudent,
    IsSubscribedFaculty,
    IsSubscribedStudent,
    IsUserItSelf,
)
from utils.response_handler import ResponseMsg as rm

from .models import User
from .serializers import (
    ActivateAccountEmailSendSerializer,
    ActivateAccountSerializer,
    ForgotpasswordEmailSendSerializer,
    ForgotpasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

# Create your views here.


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="User Login Successfully!!!")
        return Response(response.response)


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="New Access Token Get Successfully!!!")
        return Response(response.response)


class UserManager(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        if self.action == "list":
            self.permission_classes = [IsAdmin]
        if self.action in ["update", "retrieve", "partial_update", "destroy"]:
            self.permission_classes = [IsAdmin | IsUserItSelf]
        return super(UserManager, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            self.serializer_class = UserUpdateSerializer
        return super(UserManager, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="Get All User Successfully!!!")
        return Response(response.response)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="Get User Successfully!!!")
        return Response(response.response)

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="New Account Create Successfully!!!")
        return Response(response.response)

    def partial_update(self, request, *args, **kwargs):
        response_data = super().partial_update(request, *args, **kwargs)
        response = rm(data=response_data.data, error=False, message="Update Successfully!!!")
        return Response(response.response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="account-activate-email-send",
        permission_classes=[permissions.AllowAny],
        serializer_class=ActivateAccountEmailSendSerializer,
    )
    def account_email_send(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_mail()
        response = rm(data={}, error=False, message="Activation Email Send Successfully!!!")
        return Response(response.response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="account-activate",
        permission_classes=[permissions.AllowAny],
        serializer_class=ActivateAccountSerializer,
    )
    def account_activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_active()
        response = rm(data={}, error=False, message="Account Acticated!!!")
        return Response(response.response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="forgot-password-email-send",
        permission_classes=[permissions.AllowAny],
        serializer_class=ForgotpasswordEmailSendSerializer,
    )
    def forgot_password_email_send(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_mail()
        response = rm(data={}, error=False, message="Forgot password Email Send Successfully!!!")
        return Response(response.response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="forgot-password",
        permission_classes=[permissions.AllowAny],
        serializer_class=ForgotpasswordSerializer,
    )
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_password(password=request.data["password"])
        response = rm(data={}, error=False, message="Password Set Successfully!!!")
        return Response(response.response)

    @action(
        methods=["POST"],
        detail=False,
        url_path="reset-password",
        permission_classes=[IsUserItSelf],
        serializer_class=ResetPasswordSerializer,
    )
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.set_password()
        response = rm(data={}, error=False, message="Password reset Successfully!!!")
        return Response(response.response)
