from django.urls import path,include
from .views import (
    LoginView,
    RefreshTokenView,
    UserManager
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('usermanager', UserManager)

urlpatterns = [
    path('user/', include(router.urls)),
    path('login', LoginView.as_view()),
    path('refresh_view', RefreshTokenView.as_view())
]
