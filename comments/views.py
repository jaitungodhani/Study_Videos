from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdmin, IsSubscribedStudent, IsUserItSelfforComment
from utils.response_handler import ResponseMsg

from .models import Comments
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)


# Create your views here.
class ManageCommentView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Comments.objects.order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsSubscribedStudent | IsAdmin]

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsUserItSelfforComment]
        return super(ManageCommentView, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CommentCreateSerializer
        if self.action in ["update", "partial_update"]:
            self.serializer_class = CommentUpdateSerializer
        return super(ManageCommentView, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Comment Create Successfully!!")
        return Response(response.response)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        response = ResponseMsg(data=response_data.data, error=False, message="Comment update Successfully!!")
        return Response(response.response)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = ResponseMsg(data={}, error=False, message="Comment delete Successfully!!")
        return Response(response.response)

    def perform_destroy(self, instance):
        print("delete objects!!!!")
        instance.soft_delete()

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter("video_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)]
    )
    @action(
        methods=["GET"],
        detail=False,
        url_name="comment_baseon_videoid",
        permission_classes=[permissions.IsAuthenticated],
    )
    def comment_baseon_videoid(self, request):
        video_id = request.GET.get("video_id")
        queryset = Comments.objects.filter(video__id=video_id).all().order_by("-created_at")
        serializer = CommentSerializer(queryset, many=True)
        response = ResponseMsg(data=serializer.data, error=False, message="Comment fetch Successfully!!")
        return Response(response.response)
