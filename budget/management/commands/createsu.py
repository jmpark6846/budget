from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        ADMIN_NAME = os.environ['ADMIN_NAME']
        ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

        if not User.objects.filter(username=ADMIN_NAME).exists():
            User.objects.create_superuser(ADMIN_NAME, "admin@admin.com", ADMIN_PASSWORD)
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))