"""
Context processors for Django templates.
Provides site-wide template variables.
"""
from django.conf import settings


def site_urls(request):
    """
    Inject site URLs into all templates.
    
    Usage in templates:
        {{ chainlit_url }}
        {{ django_url }}
    """
    return {
        'chainlit_url': settings.CHAINLIT_URL,
        'django_url': settings.DJANGO_URL,
    }
