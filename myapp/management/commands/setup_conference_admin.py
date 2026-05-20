from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


ADMIN_EMAIL = "sjkarthikeyans2008@gmail.com"


class Command(BaseCommand):
    help = "Create or update the private ICGB admin login."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            help="Admin password. If omitted, the command will ask for it securely.",
        )

    def handle(self, *args, **options):
        password = options.get("password")
        if not password:
            password = getpass("Admin password: ")
            confirm = getpass("Confirm password: ")
            if password != confirm:
                raise CommandError("Passwords do not match.")

        if len(password) < 8:
            raise CommandError("Use a password with at least 8 characters.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=ADMIN_EMAIL,
            defaults={"email": ADMIN_EMAIL, "is_staff": True, "is_superuser": True},
        )
        user.email = ADMIN_EMAIL
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Admin login {action}: {ADMIN_EMAIL}"))
