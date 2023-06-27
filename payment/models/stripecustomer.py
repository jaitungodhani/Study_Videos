from django.db import models
from account.models import User
from study_videos.behaviors import DateMixin


class StripeCustomer(DateMixin, models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
