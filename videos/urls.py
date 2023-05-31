from django.urls import path,include
from .views import (
    ManageVideos,
    ManageThumbnaailsView,
    ManageVideoChannelView,
    ManageVideoFileView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('managevideos', ManageVideos)
router.register('managechannel', ManageVideoChannelView)
router.register('managevideofile', ManageVideoFileView)
router.register('managethumbnai', ManageThumbnaailsView)

urlpatterns = [
    path('videos/', include(router.urls))
]
