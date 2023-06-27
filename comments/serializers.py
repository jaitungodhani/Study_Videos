from rest_framework import serializers
from .models import Comments
from videos.serializers import VideosSerializer
from account.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("text", "video", "parent")

    def validate_parent(self, parent):
        return parent.get_root()

    def to_representation(self, instance):
        return CommentSerializer(instance).data


class CommentUpdateSerializer(CommentCreateSerializer):
    class Meta(CommentCreateSerializer.Meta):
        extra_kwargs = {"user": {"read_only": True}, "video": {"read_only": True}}
