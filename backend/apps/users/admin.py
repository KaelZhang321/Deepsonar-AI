"""Admin configuration for the users app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with additional fields."""

    list_display = (
        "username",
        "email",
        "company",
        "api_calls_count",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "company")

    # Add custom fields to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("company", "api_calls_count")}),
    )
