# Generated by Django 4.2.1 on 2023-06-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="cognito_id",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="cognito_id"),
        ),
    ]
