from django.contrib import admin
from .models import Videos, Video_Channel, VideosFile, Video_Thumbnails

# Register your models here.


@admin.register(Video_Channel)
class VideoChannelAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "for_channel"]
    search_fields = ["title", "description"]


@admin.register(VideosFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Video_Thumbnails)
class VideoThumbnailAdmin(admin.ModelAdmin):
    list_display = ["id", "video_file", "is_active"]
