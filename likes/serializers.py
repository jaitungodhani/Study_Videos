from rest_framework import serializers

from .models import Likes


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}
