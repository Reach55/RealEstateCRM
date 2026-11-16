import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the initial CRM administrator from deployment environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

        if not username or not password:
            self.stdout.write('Initial admin credentials are not configured; skipping.')
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Initial admin {username!r} already exists; skipping.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='ADMIN',
        )
        self.stdout.write(self.style.SUCCESS(f'Created initial admin {username!r}.'))
