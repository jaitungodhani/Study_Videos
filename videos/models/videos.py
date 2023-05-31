from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from study_videos.behaviors import DateMixin
from .video_channel import Video_Channel
from .video_file import VideosFile
# Create your models here.

class Videos(DateMixin, models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255
    )
    description = models.TextField(
        verbose_name=_("description"),
        null=True,
        blank=True
    )
    video_file = models.OneToOneField(
        VideosFile,
        verbose_name=_("Video File"),
        related_name="video_data",
        on_delete=models.CASCADE
    )
    is_subscribed = models.BooleanField(
        verbose_name=_("is subscribed"),
        default=True
    )
    for_channel = models.ForeignKey(
        Video_Channel,
        verbose_name= _("Video Channel"),
        on_delete= models.CASCADE,
        null=True
    )
    is_publish = models.BooleanField(
        verbose_name=_("Is Publish"),
        default=False
    )
    file_name = models.CharField(
        verbose_name=_("File Name"),
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ["created_at"]

    