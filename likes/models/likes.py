from django.db import models
from account.models import User
from videos.models import Videos
from study_videos.behaviors import DateMixin
from django.utils.translation import gettext_lazy as _

class Likes(DateMixin, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_for_like"
    )
    videos = models.ForeignKey(
        Videos,
        verbose_name=_("Videos"),
        on_delete=models.CASCADE,
        related_name="video_for_like"
    )

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ('user', 'videos')

    def __str__(self) -> str:
        return str(self.user.id) + "----" + str(self.videos.id)
