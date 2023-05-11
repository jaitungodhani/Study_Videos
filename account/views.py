from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .serializers import (
    LoginSerializer
)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from utils.response_handler import ResponseMsg as rm
from rest_framework.response import Response


# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response_data =  super().post(request, *args, **kwargs)
        response = rm(
            data = response_data.data,
            error=False,
            message="User Login Successfully!!!"
        )
        return Response(response.response)
    
class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs)
        response = rm(
            data = response_data.data,
            error=False,
            message="New Access Token Get Successfully!!!"
        )
        return Response(response.response)
