"""
URL configuration for AI Business Data Analysis Platform.

Includes Django Ninja API router.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

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
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
