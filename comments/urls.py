from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ManageCommentView

router = DefaultRouter()

router.register("managecomments", ManageCommentView)

urlpatterns = [path("comments/", include(router.urls))]
