"""
URL configuration for AI Business Data Analysis Platform.

Includes Django Ninja API router and authentication views.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.users.views import (
    home, login_view, register_view, logout_view,
    reports_list, report_detail, 
    report_export_markdown, report_export_word, report_export_pdf
)

# Initialize Django Ninja API
api = NinjaAPI(
    title="AI Business Analysis API",
    description="API for AI-powered business data analysis and report generation",
    version="1.0.0",
)


# Health check endpoint
@api.get("/health")
def health_check(request) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# Trial application endpoint
from ninja import Schema
from apps.users.trial_models import TrialApplication

class TrialApplicationSchema(Schema):
    name: str
    email: str
    organization: str
    title: str = ""
    useCase: str = "market_analysis"
    message: str = ""

@api.post("/trial-application")
def submit_trial_application(request, data: TrialApplicationSchema):
    """Submit a trial application from the portal."""
    application = TrialApplication.objects.create(
        name=data.name,
        email=data.email,
        organization=data.organization,
        title=data.title,
        use_case=data.useCase,
        message=data.message,
    )
    return {"success": True, "id": application.id}



urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API
    path("api/", api.urls),
    
    # Auth & Frontend
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    
    # Reports
    path("reports/", reports_list, name="reports_list"),
    path("reports/<int:report_id>/", report_detail, name="report_detail"),
    path("reports/<int:report_id>/export/md/", report_export_markdown, name="report_export_md"),
    path("reports/<int:report_id>/export/word/", report_export_word, name="report_export_word"),
    path("reports/<int:report_id>/export/pdf/", report_export_pdf, name="report_export_pdf"),
    
    # Catch-all for React frontend routes (must be last)
    path("", home, name="home"),
]

# Add catch-all pattern for React Router paths
from django.urls import re_path
urlpatterns += [
    re_path(r'^(?!admin|api|login|register|logout|reports|static).*$', home, name="frontend_catchall"),
]



