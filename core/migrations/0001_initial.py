# Generated by Django 4.2.1 on 2023-05-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=5, verbose_name="Code")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Name")),
                ("native_name", models.CharField(blank=True, default="", max_length=255, verbose_name="Native Name")),
            ],
            options={
                "verbose_name": "Language",
                "verbose_name_plural": "Languages",
                "ordering": ("name",),
            },
        ),
    ]
