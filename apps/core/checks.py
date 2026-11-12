from django.conf import settings
from django.core.checks import Error, Tags, register

from .turnstile import TEST_SITE_KEYS


@register(Tags.security, deploy=True)
def production_services_configured(app_configs, **kwargs):
    """Run by `manage.py check --deploy`: production must not use test or console services."""
    errors = []
    if not settings.TURNSTILE_SECRET_KEY or settings.TURNSTILE_SITE_KEY in TEST_SITE_KEYS:
        errors.append(
            Error(
                "Cloudflare Turnstile is using test keys or no keys.",
                hint="Set TURNSTILE_SITE_KEY and TURNSTILE_SECRET_KEY.",
                id="core.E001",
            )
        )
    if settings.EMAIL_BACKEND.endswith((".console.EmailBackend", ".locmem.EmailBackend")):
        errors.append(
            Error(
                "Email is not sent to a real provider.",
                hint="Set EMAIL_URL to the transactional email provider's SMTP URL.",
                id="core.E002",
            )
        )
    return errors
