from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ['ADMIN_NAME']).exists():
            User.objects.create_superuser(os.environ['ADMIN_NAME'], "admin@admin.com", os.environ['ADMIN_PASSWORD'])
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))