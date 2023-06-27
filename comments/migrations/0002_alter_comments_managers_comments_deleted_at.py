# Generated by Django 4.2.1 on 2023-06-25 05:59

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="comments",
            managers=[
                ("_tree_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="comments",
            name="deleted_at",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
