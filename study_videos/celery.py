import os

from celery import Celery
from django.core.mail import EmailMessage
from decouple import config


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "study_videos.settings")

app = Celery("study_videos")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def send_mail(self, subject, body, recipient, content_subtype="html"):

    mail = EmailMessage(
        subject,
        body,
        config("EMAIL_ID"),
        [recipient],
    )
    mail.content_subtype = "html"
    return mail.send(fail_silently=False)
