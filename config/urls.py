from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import SITEMAPS
from apps.core.views import robots_txt, security_txt

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", robots_txt),
    path(".well-known/security.txt", security_txt),
    path("", include("apps.messaging.urls")),
    path("", include("apps.programmes.urls")),
    path("", include("apps.recruitment.urls")),
    path("", include("apps.legal.urls")),
    path("", include("apps.core.urls")),
]

handler500 = "apps.core.views.server_error"
