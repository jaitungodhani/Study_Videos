from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User
from videos.models import Videos
from mptt.models import MPTTModel, TreeForeignKey
from study_videos.behaviors import DateMixin, SoftDeleteMixin


class Comments(DateMixin, SoftDeleteMixin, MPTTModel):
    text = models.TextField(verbose_name=_("Text"))
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_for_comment")
    video = models.ForeignKey(
        Videos, verbose_name=_("Video"), on_delete=models.CASCADE, related_name="video_for_comment"
    )
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self) -> str:
        return str(self.user.id) + "---" + str(self.video.id)
