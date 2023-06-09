import os

from django.core.files.images import ImageFile
from rest_framework import serializers

from account.serializers import UserSerializer
from comments.models import Comments
from likes.models import Likes

from .helpers import generate_thumbnail
from .models import Video_Channel, Video_Thumbnails, Videos, VideosFile


class ThumbnaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video_Thumbnails
        fields = "__all__"


class VideoFileBaseSerializer(serializers.ModelSerializer):
    video_for_thumbnails = ThumbnaisSerializer(many=True, read_only=True)

    class Meta:
        model = VideosFile
        fields = "__all__"
        extra_kwargs = {"uploaded_by": {"read_only": True}}

    def validate_video_file(self, value):
        self.file = value
        self.file_name = value.name
        if not self.file_name.lower().endswith(".mp4"):
            raise serializers.ValidationError("Only Upload .mp4 file")
        return value

    def create(self, validated_data):
        new_obj = VideosFile.objects.create(**validated_data)
        file_name, ext = os.path.splitext(new_obj.video_file.name)
        file_name = file_name.split("/")[1]

        generate_thumbnail(
            in_filename=new_obj.video_file.url,
            out_filename1="%s1.jpeg" % file_name,
            out_filename2="%s2.jpeg" % file_name,
            out_filename3="%s3.jpeg" % file_name,
        )
        Video_Thumbnails.objects.create(
            image=ImageFile(open("%s1.jpeg" % file_name, "rb")), video_file=new_obj, is_active=True
        )
        Video_Thumbnails.objects.create(
            image=ImageFile(open("%s2.jpeg" % file_name, "rb")), video_file=new_obj, is_active=False
        )
        Video_Thumbnails.objects.create(
            image=ImageFile(open("%s3.jpeg" % file_name, "rb")), video_file=new_obj, is_active=False
        )
        if os.path.exists("%s1.jpeg" % file_name):
            os.remove("%s1.jpeg" % file_name)
        if os.path.exists("%s2.jpeg" % file_name):
            os.remove("%s2.jpeg" % file_name)
        if os.path.exists("%s3.jpeg" % file_name):
            os.remove("%s3.jpeg" % file_name)

        return new_obj


class VideoFileSerilaizer(VideoFileBaseSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)

    def get_title(self, obj):
        file_name, _ = os.path.splitext(self.file_name)
        return file_name

    def get_file_name(self, obj):
        return self.file_name


class VideoChannelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Video_Channel
        fields = "__all__"


class VideoChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video_Channel
        fields = "__all__"
        extra_kwargs = {"created_by": {"read_only": True}}

    def to_representation(self, instance):
        return VideoChannelSerializer(instance).data


class VideosSerializer(serializers.ModelSerializer):
    for_channel = VideoChannelSerializer(read_only=True)
    video_file = VideoFileBaseSerializer(read_only=True)
    num_of_likes = serializers.SerializerMethodField(read_only=True)
    like_by_user = serializers.SerializerMethodField(read_only=True)
    num_of_comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Videos
        fields = "__all__"

    def get_num_of_likes(self, obj):
        return Likes.objects.filter(videos__id=obj.id).count()

    def get_num_of_comments(self, obj):
        return Comments.objects.filter(video__id=obj.id).count()

    def get_like_by_user(self, obj):
        return Likes.objects.filter(videos__id=obj.id, user=self.context["request"].user).exists()


class VideosCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = "__all__"

    def to_representation(self, instance):
        return VideosSerializer(instance, context={"request": self.context["request"]}).data


class ThumbnailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video_Thumbnails
        exclude = ("image", "video_file")

    def to_representation(self, instance):
        return ThumbnaisSerializer(instance).data
