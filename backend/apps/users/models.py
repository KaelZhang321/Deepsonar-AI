"""
Custom User model for AI Business Data Analysis Platform.

Extends Django's AbstractUser to allow future customization.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model.

    Extends AbstractUser to enable future customization such as:
    - API key storage
    - Usage tracking
    - Organization/team membership
    """

    # Optional: Add custom fields here
    company: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        help_text="User's company or organization name"
    )
    api_calls_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Number of API calls made by this user"
    )

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username
