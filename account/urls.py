from django.urls import path
from .views import (
    LoginView,
    RefreshTokenView
)


urlpatterns = [
    path('login', LoginView.as_view()),
    path('refresh_view', RefreshTokenView.as_view())
]
