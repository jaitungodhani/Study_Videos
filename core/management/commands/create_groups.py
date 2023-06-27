from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

GROUPS = ["Admin", "Faculty", "Subscribed Faculty", "Student", "Subscribed Student"]


class Command(BaseCommand):
    help = "Create Groups"

    def handle(self, *args, **kwargs):
        for group in GROUPS:
            try:
                Group.objects.get_or_create(name=group)
            except Exception as e:
                raise CommandError(str(e))

        print("All Groups Create Successfully!!")
