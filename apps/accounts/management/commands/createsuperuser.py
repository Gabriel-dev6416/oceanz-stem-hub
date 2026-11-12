import os

from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import CommandError


class Command(createsuperuser.Command):
    """Django's createsuperuser, with a clear message when the email is already in use.

    Emails are unique ignoring case (accounts_user_email_unique_ci). Interactive runs ask for
    the email again; non-interactive runs stop with an error before anything is saved.
    """

    def email_in_use(self, email):
        return bool(email) and self.UserModel._default_manager.filter(email__iexact=email).exists()

    def get_input_data(self, field, message, default=None):
        value = super().get_input_data(field, message, default)
        if field.name == "email" and self.email_in_use(value):
            self.stderr.write("Error: That email address is already in use.")
            return None  # Django asks for the field again.
        return value

    def handle(self, *args, **options):
        if not options["interactive"]:
            email = options.get("email") or os.environ.get("DJANGO_SUPERUSER_EMAIL")
            if self.email_in_use(email):
                raise CommandError("That email address is already in use.")
        return super().handle(*args, **options)
