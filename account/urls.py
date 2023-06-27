from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, RefreshTokenView, UserManager

router = DefaultRouter()

router.register("usermanager", UserManager)

urlpatterns = [
    path("user/", include(router.urls)),
    path("login", LoginView.as_view()),
    path("refresh_view", RefreshTokenView.as_view()),
]
