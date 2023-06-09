# Generated by Django 4.2.1 on 2023-05-30 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0007_videos_file_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videos",
            name="video_file",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video_data",
                to="videos.videosfile",
                verbose_name="Video File",
            ),
        ),
    ]
