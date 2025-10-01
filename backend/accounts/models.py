"""Database models for the accounts app."""
from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Application user model using email as the unique identifier."""

    username = None  # remove username field
    email = models.EmailField("email address", unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True, validators=[URLValidator()])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.display_name or self.email

    @property
    def safe_display_name(self) -> str:
        """Return a friendly name that always has a value."""

        return self.display_name or self.email.split("@")[0]
