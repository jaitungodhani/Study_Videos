# Generated by Django 4.2.1 on 2023-06-25 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_user_cognito_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="cognito_id",
        ),
    ]
