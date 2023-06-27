from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from study_videos.behaviors import DateMixin

from .video_file import VideosFile


class Video_Thumbnails(DateMixin, models.Model):
    image = models.ImageField(verbose_name=_("Video Thumbnail"), upload_to="thumbnails")
    video_file = models.ForeignKey(
        VideosFile, verbose_name=_("Video File"), on_delete=models.CASCADE, related_name="video_for_thumbnails"
    )
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = "Video Thumbnail"
        verbose_name_plural = "Video Thumbnails"
