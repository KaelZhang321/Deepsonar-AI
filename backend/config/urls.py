"""
URL configuration for AI Business Data Analysis Platform.

Includes Django Ninja API router and authentication views.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.users.views import (
    home, login_view, register_view, logout_view,
    reports_list, report_detail, report_export_markdown
)

# Initialize Django Ninja API
api = NinjaAPI(
    title="AI Business Analysis API",
    description="API for AI-powered business data analysis and report generation",
    version="1.0.0",
)


# Example endpoint - can be extended with more routes
@api.get("/health")
def health_check(request) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API
    path("api/", api.urls),
    
    # Auth & Frontend
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    
    # Reports
    path("reports/", reports_list, name="reports_list"),
    path("reports/<int:report_id>/", report_detail, name="report_detail"),
    path("reports/<int:report_id>/export/", report_export_markdown, name="report_export"),
]


