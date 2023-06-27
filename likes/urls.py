from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LikesView

router = DefaultRouter()

router.register("managelikes", LikesView)

urlpatterns = [path("likes/", include(router.urls))]
