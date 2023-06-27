from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, views, viewsets
from rest_framework.response import Response

from core.permissions import (
    IsAdmin,
    IsFaculty,
    IsSubscribedFaculty,
    IsUserItSelfforThumnails,
    IsUserItSelfforVideos,
    IsUserItSelfforVideosChannel,
    IsUserItSelfforVideosFileUpload,
)
from utils.response_handler import ResponseMsg

from .models import Video_Channel, Video_Thumbnails, Videos, VideosFile
from .serializers import (
    ThumbnailUpdateSerializer,
    VideoChannelCreateSerializer,
    VideoChannelSerializer,
    VideoFileSerilaizer,
    VideosCreateSerializer,
    VideosSerializer,
)

# Create your views here.


class ManageVideoChannelView(viewsets.ModelViewSet):
    queryset = Video_Channel.objects.order_by("created_at")
    serializer_class = VideoChannelSerializer
    permission_classes = [IsFaculty | IsSubscribedFaculty | IsAdmin]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsSubscribedFaculty | IsAdmin]
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsUserItSelfforVideosChannel]
        return super(ManageVideoChannelView, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_subscribedfacultyuser or self.request.user.is_facultyuser:
                return self.queryset.filter(created_by=self.request.user).all()
        return super(ManageVideoChannelView, self).get_queryset()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            self.serializer_class = VideoChannelCreateSerializer
        return super(ManageVideoChannelView, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels Get Successfully!!!")
        return Response(response.response)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels Detail Get Successfully!!!")
        return Response(response.response)

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels Create Successfully!!!")
        return Response(response.response)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels update Successfully!!!")
        return Response(response.response)

    def partial_update(self, request, *args, **kwargs):
        response_data = super().partial_update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels Partial Update Successfully!!!")
        return Response(response.response)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = ResponseMsg(data={}, error=False, message="Delete Channel Successfully!!!")
        return Response(response.response)


class ManageVideoFileView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = VideosFile.objects.order_by("created_at")
    serializer_class = VideoFileSerilaizer
    permission_classes = [IsSubscribedFaculty | IsAdmin]

    def get_permissions(self):
        if self.action in ["destroy"]:
            self.permission_classes = [IsUserItSelfforVideosFileUpload]
        return super(ManageVideoFileView, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_subscribedfacultyuser:
                return self.queryset.filter(uploaded_by=self.request.user).all()
        return super(ManageVideoFileView, self).get_queryset()

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Channels Create Successfully!!!")
        return Response(response.response)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = ResponseMsg(data={}, error=False, message="Delete Channel Successfully!!!")
        return Response(response.response)


class ManageVideos(viewsets.ModelViewSet):
    queryset = Videos.objects.all().order_by("-created_at")
    serializer_class = VideosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description", "for_channel__name", "for_channel__created_by__username"]
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdmin | IsSubscribedFaculty]
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsUserItSelfforVideos]
        return super(ManageVideos, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_facultyuser or self.request.user.is_subscribedfacultyuser:
                return self.queryset.filter(uploaded_by=self.request.user, is_publish=True).all()
            if self.request.user.is_adminuser or self.request.user.is_subscribedstudentuser:
                return self.queryset
        return self.queryset.filter(is_subscribed=False, is_publish=True).all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            self.serializer_class = VideosCreateSerializer
        return super(ManageVideos, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="All Videos get Successfully!!!")
        return Response(response.response)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Video detail get Successfully!!!")
        return Response(response.response)

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Video create Successfully!!!")
        return Response(response.response)

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Video update Successfully!!!")
        return Response(response.response)

    def partial_update(self, request, *args, **kwargs):
        response_data = super().partial_update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Video update Successfully!!!")
        return Response(response.response)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = ResponseMsg(data={}, error=False, message="Video delete Successfully!!!")
        return Response(response.response)


class ManageThumbnaailsView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Video_Thumbnails.objects.all()
    serializer_class = ThumbnailUpdateSerializer
    permission_classes = [IsUserItSelfforThumnails]

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Thumbnail Status Update Successfully!!!")
        return Response(response.response)
