from django.db import models
from django.utils.translation import gettext_lazy as _
from study_videos.behaviors import DateMixin
from account.models import User

# Create your models here.

class VideosFile(DateMixin, models.Model):
    video_file = models.FileField(
        verbose_name=_("Video File"),
        upload_to="videos"
    )
    uploaded_by = models.ForeignKey(
        User,
        verbose_name=_("Uploaded By"),
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name = _("VideoFile")
        verbose_name_plural = _("VideosFiles")
        ordering = ["created_at"]