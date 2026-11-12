import pytest
from django.core.management import CommandError, call_command
from django.db import IntegrityError

from .management.commands.createsuperuser import Command as CreateSuperuserCommand
from .models import User


@pytest.mark.django_db
def test_email_is_unique_ignoring_case():
    User.objects.create_user(username="ada", email="Ada@Example.com", password="x" * 12)

    with pytest.raises(IntegrityError):
        User.objects.create_user(username="ada2", email="ada@example.com", password="x" * 12)


@pytest.mark.django_db
def test_accounts_without_email_are_allowed():
    User.objects.create_user(username="child1", password="x" * 12)
    User.objects.create_user(username="child2", password="x" * 12)

    assert User.objects.filter(email="").count() == 2


@pytest.mark.django_db
def test_public_id_is_assigned_and_unique():
    first = User.objects.create_user(username="first", password="x" * 12)
    second = User.objects.create_user(username="second", password="x" * 12)

    assert first.public_id != second.public_id


@pytest.mark.django_db
def test_passwords_are_hashed_with_argon2():
    user = User.objects.create_user(username="hashcheck", password="x" * 12)

    assert user.password.startswith("argon2")


@pytest.mark.django_db
def test_createsuperuser_rejects_email_in_use_without_traceback():
    User.objects.create_superuser("owner", "Owner@Example.com", "x" * 12)

    with pytest.raises(CommandError, match="email address is already in use"):
        call_command("createsuperuser", "--noinput", username="second", email="owner@example.com")

    assert not User.objects.filter(username="second").exists()


@pytest.mark.django_db
def test_createsuperuser_email_check_ignores_case():
    User.objects.create_user("ada", "ada@example.com", "x" * 12)
    command = CreateSuperuserCommand()

    assert command.email_in_use("ADA@example.com")
    assert not command.email_in_use("someone@example.com")
    assert not command.email_in_use("")
