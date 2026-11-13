import logging

from django.core.cache import cache
from django.db import connection
from django.db.models import Min
from django.http import Http404, HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from apps.programmes.forms import ExplorerForm
from apps.programmes.models import HolidaySession, Level, TertiaryPackage

from .models import FAQ, AboutPage, FeatureCard, HomePage, SiteSettings, Stat, Testimonial

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


def _organisation(request, faqs):
    """schema.org data for search engines (SRS 8.5): EducationalOrganization and FAQPage."""
    site = SiteSettings.load()
    home_url = request.build_absolute_uri(reverse("core:home"))
    organisation = {
        "@type": "EducationalOrganization",
        "name": "OCEANZ STEM HUB",
        "url": home_url,
        "logo": request.build_absolute_uri(static("img/apple-touch-icon.png")),
        "email": site.email,
        "telephone": site.phone_primary,
        "sameAs": [url for _, url in site.social_links],
    }
    if site.address:
        organisation["address"] = {
            "@type": "PostalAddress",
            "streetAddress": site.address,
            "addressCountry": "NG",
        }
    graph = [organisation]
    if faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq.question,
                        "acceptedAnswer": {"@type": "Answer", "text": faq.answer},
                    }
                    for faq in faqs
                ],
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def home(request):
    faqs = list(FAQ.objects.filter(published=True))
    return render(
        request,
        "core/home.html",
        {
            "structured_data": _organisation(request, faqs),
            "page_title": "Home",
            "home": HomePage.load(),
            "features": FeatureCard.objects.filter(published=True),
            "stats": Stat.objects.filter(published=True),
            "faqs": faqs,
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


def about(request):
    return render(request, "core/about.html", {"page_title": "About us", "about": AboutPage.load()})


def diaspora(request):
    """Families abroad (FR-ENG-12). Their fees are quoted, never published (FR-PAY-13)."""
    return render(request, "core/diaspora.html", {"page_title": "Families abroad"})


def results(request):
    """Verified figures entered by the Admin (FR-WEB-06). No page until there are some."""
    stats = Stat.objects.filter(published=True)
    if not stats:
        raise Http404
    return render(request, "core/results.html", {"page_title": "Results", "stats": stats})


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /enquire/received/",
        "Disallow: /teach-with-us/thanks/",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return _text_response(lines)


@require_GET
def security_txt(request):
    """RFC 9116 security contact (SRS section 11)."""
    expires = (timezone.now() + timezone.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    lines = [
        f"Contact: mailto:{SiteSettings.load().email}",
        f"Expires: {expires}",
        "Preferred-Languages: en",
        f"Canonical: {request.build_absolute_uri()}",
    ]
    return _text_response(lines)


def _text_response(lines):
    return HttpResponse("".join(f"{line}\n" for line in lines), content_type="text/plain")


def server_error(request):
    """500 page rendered without the database or context processors, which may be the fault."""
    number = SiteSettings._meta.get_field("whatsapp").default
    return HttpResponseServerError(
        loader.get_template("500.html").render({"whatsapp_number": number})
    )
