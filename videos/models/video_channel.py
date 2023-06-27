from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from account.models import User
from study_videos.behaviors import DateMixin


class Video_Channel(DateMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=_("Channel Name"), max_length=255, unique=True)
    created_by = models.ForeignKey(User, verbose_name=_("Created By"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = _("Videos Channel")
        verbose_name_plural = _("Videos Channels")
        ordering = ("created_at",)
