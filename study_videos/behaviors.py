from django.db import models



class DateMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False
    )

    class Meta:
        abstract = True