"""Admin configuration for the reports app."""
from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin configuration for Report model."""

    list_display = (
        "id",
        "query_preview",
        "user",
        "status",
        "created_at",
        "completed_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("query", "output", "user__username")
    readonly_fields = ("created_at", "completed_at")
    ordering = ("-created_at",)

    @admin.display(description="Query")
    def query_preview(self, obj: Report) -> str:
        """Display truncated query in list view."""
        return obj.query[:50] + "..." if len(obj.query) > 50 else obj.query
