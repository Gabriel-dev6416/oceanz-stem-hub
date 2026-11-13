from django.conf import settings

from .models import SiteSettings, Stat


def site(request):
    return {
        "site_settings": SiteSettings.load(),
        "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        "has_results": Stat.objects.filter(published=True).exists(),
    }
