# Generated by Django 4.2.1 on 2023-05-30 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0006_videos_is_publish"),
    ]

    operations = [
        migrations.AddField(
            model_name="videos",
            name="file_name",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="File Name"),
        ),
    ]
