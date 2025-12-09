"""Admin configuration for the reports app."""
from django.contrib import admin

from .models import Report, ChatSession, ChatMessage


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


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Admin configuration for ChatSession model."""
    
    list_display = ("id", "user", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "user__username")
    ordering = ("-created_at",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin configuration for ChatMessage model."""
    
    list_display = ("id", "session", "sender", "content_preview", "timestamp")
    list_filter = ("sender", "timestamp")
    search_fields = ("content",)
    ordering = ("-timestamp",)
    
    @admin.display(description="Content")
    def content_preview(self, obj: ChatMessage) -> str:
        """Display truncated content in list view."""
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content

