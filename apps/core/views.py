import logging

from django.core.cache import cache
from django.db import connection
from django.db.models import Min
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from apps.programmes.forms import ExplorerForm
from apps.programmes.models import HolidaySession, Level, TertiaryPackage

from .models import FAQ, FeatureCard, HomePage, SiteSettings, Stat, Testimonial

logger = logging.getLogger(__name__)


def _database_ok():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)
    except Exception:
        logger.exception("Health check: database unavailable")
        return False


def _cache_ok():
    try:
        cache.set("health:ping", "pong", timeout=5)
        return cache.get("health:ping") == "pong"
    except Exception:
        logger.exception("Health check: cache unavailable")
        return False


@never_cache
@require_GET
def health(request):
    """Liveness and dependency check used by Render and uptime monitoring (NFR-15)."""
    checks = {
        "database": "ok" if _database_ok() else "error",
        "cache": "ok" if _cache_ok() else "error",
    }
    healthy = all(value == "ok" for value in checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "error", "checks": checks},
        status=200 if healthy else 503,
    )


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "page_title": "Home",
            "home": HomePage.load(),
            "features": FeatureCard.objects.filter(published=True),
            "stats": Stat.objects.filter(published=True),
            "faqs": FAQ.objects.filter(published=True),
            "testimonials": Testimonial.objects.filter(published=True, consent_confirmed=True),
            "explorer_form": ExplorerForm(),
            "levels": Level.objects.filter(published=True),
            "sessions": HolidaySession.objects.filter(published=True),
            "packages": TertiaryPackage.objects.filter(published=True),
            "term_from": Level.objects.filter(published=True).aggregate(m=Min("term_fee"))["m"],
            "holiday_from": HolidaySession.objects.filter(published=True).aggregate(m=Min("fee"))[
                "m"
            ],
        },
    )


def server_error(request):
    """500 page rendered without the database or context processors, which may be the fault."""
    number = SiteSettings._meta.get_field("whatsapp").default
    return HttpResponseServerError(
        loader.get_template("500.html").render({"whatsapp_number": number})
    )
