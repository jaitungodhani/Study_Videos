from django.urls import path, include
from .views import ManageCommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("managecomments", ManageCommentView)

urlpatterns = [path("comments/", include(router.urls))]
