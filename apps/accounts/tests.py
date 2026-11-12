import pytest
from django.db import IntegrityError

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
