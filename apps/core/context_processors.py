from django.conf import settings

from .models import SiteSettings


def site(request):
    return {
        "site_settings": SiteSettings.load(),
        "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
    }
