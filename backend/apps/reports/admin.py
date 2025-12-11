"""Admin configuration for the reports app."""
from django.contrib import admin

from .models import Report, ChatSession, ChatMessage, SearchResult


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin configuration for Report model."""

    list_display = (
        "id",
        "query_preview",
        "user",
        "user_id_display",
        "status",
        "created_at",
        "completed_at",
    )
    list_filter = ("status", "created_at", "user")
    search_fields = ("query", "output", "user__username")
    readonly_fields = ("created_at", "completed_at")
    ordering = ("-created_at",)
    
    # 可以直接编辑用户关联
    raw_id_fields = ("user",)

    @admin.display(description="Query")
    def query_preview(self, obj: Report) -> str:
        """Display truncated query in list view."""
        return obj.query[:50] + "..." if len(obj.query) > 50 else obj.query
    
    @admin.display(description="User ID")
    def user_id_display(self, obj: Report) -> str:
        """Display user ID or warning if not set."""
        if obj.user:
            return str(obj.user.id)
        return "⚠️ NULL"


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


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    """Admin configuration for SearchResult model."""
    
    list_display = (
        "id",
        "keyword_preview",
        "results_count",
        "search_source",
        "report",
        "created_at",
    )
    list_filter = ("search_source", "created_at")
    search_fields = ("keyword", "formatted_results")
    readonly_fields = ("created_at", "results_json", "formatted_results")
    ordering = ("-created_at",)
    
    fieldsets = (
        ("基本信息", {
            "fields": ("keyword", "search_source", "results_count", "report", "created_at")
        }),
        ("搜索结果", {
            "fields": ("formatted_results",),
            "classes": ("collapse",)
        }),
        ("原始数据", {
            "fields": ("results_json",),
            "classes": ("collapse",)
        }),
    )
    
    @admin.display(description="关键词")
    def keyword_preview(self, obj: SearchResult) -> str:
        """Display truncated keyword in list view."""
        return obj.keyword[:60] + "..." if len(obj.keyword) > 60 else obj.keyword
