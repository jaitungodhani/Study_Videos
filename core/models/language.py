from django.db import models
from django.utils.translation import gettext_lazy as _

from study_videos.behaviors import DateMixin


class Language(DateMixin, models.Model):
    code = models.CharField(verbose_name=_("Code"), max_length=5)
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    native_name = models.CharField(max_length=255, verbose_name=_("Native Name"), blank=True, default="")

    class Meta:
        ordering = ("name",)
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self) -> str:
        return self.name
