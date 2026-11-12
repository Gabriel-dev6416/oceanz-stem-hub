import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    """Platform account.

    Children under 13 sign in with a username and may have no email (FR-ACC-02), so email is
    optional but unique (case-insensitive) whenever it is set. Public URLs use public_id,
    never the sequential primary key (SEC-ACL-02).
    """

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField("email address", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                condition=~models.Q(email=""),
                name="accounts_user_email_unique_ci",
            ),
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
