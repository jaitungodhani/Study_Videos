# Generated by Django 4.2.1 on 2023-05-28 09:54

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Video_Channel",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Channel Name")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Videos Channel",
                "verbose_name_plural": "Videos Channels",
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="VideosFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("video_file", models.FileField(upload_to="videos", verbose_name="Video File")),
            ],
            options={
                "verbose_name": "VideoFile",
                "verbose_name_plural": "VideosFiles",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Videos",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("description", models.TextField(blank=True, null=True, verbose_name="description")),
                ("is_subscribed", models.BooleanField(default=True, verbose_name="is subscribed")),
                (
                    "for_channel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="videos.video_channel",
                        verbose_name="Video Channel",
                    ),
                ),
                (
                    "video_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="videos.videosfile", verbose_name="Video File"
                    ),
                ),
            ],
            options={
                "verbose_name": "Video",
                "verbose_name_plural": "Videos",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Video_Thumbnails",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("image", models.ImageField(upload_to="thumbnails/", verbose_name="Video Thumbnail")),
                ("is_active", models.BooleanField(default=False, verbose_name="Is Active")),
                (
                    "video_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="videos.videosfile", verbose_name="Video File"
                    ),
                ),
            ],
            options={
                "verbose_name": "Video Thumbnail",
                "verbose_name_plural": "Video Thumbnails",
            },
        ),
    ]
