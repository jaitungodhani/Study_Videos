from django.urls import path,include
from .views import LikesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("managelikes", LikesView)

urlpatterns = [
    path('likes/', include(router.urls))
]