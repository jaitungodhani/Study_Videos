from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ManageThumbnaailsView, ManageVideoChannelView, ManageVideoFileView, ManageVideos

router = DefaultRouter()

router.register("managevideos", ManageVideos)
router.register("managechannel", ManageVideoChannelView)
router.register("managevideofile", ManageVideoFileView)
router.register("managethumbnai", ManageThumbnaailsView)

urlpatterns = [path("videos/", include(router.urls))]
