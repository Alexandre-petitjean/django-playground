from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate bulk test data for stock management system"

    def handle(self, *args, **kwargs):
        user_class = get_user_model()

        if not user_class.objects.filter(email="admin@admin.local").exists():
            user_class.objects.create_superuser(email="admin@admin.local", password="admin")  # noqa: S106
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
