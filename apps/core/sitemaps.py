from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.legal.models import LegalPage
from apps.programmes.models import Level, TertiaryPackage


class StaticPagesSitemap(Sitemap):
    def items(self):
        return [
            "core:home",
            "core:about",
            "core:diaspora",
            "programmes:overview",
            "programmes:holiday",
            "programmes:tertiary",
            "programmes:subjects",
            "programmes:pricing",
            "programmes:explorer",
            "messaging:enquire",
            "messaging:contact",
            "recruitment:teach_with_us",
        ]

    def location(self, item):
        return reverse(item)


class LevelSitemap(Sitemap):
    def items(self):
        return Level.objects.filter(published=True)


class PackageSitemap(Sitemap):
    def items(self):
        return TertiaryPackage.objects.filter(published=True)


class LegalSitemap(Sitemap):
    def items(self):
        return LegalPage.objects.all()

    def lastmod(self, page):
        return page.updated_at


SITEMAPS = {
    "pages": StaticPagesSitemap,
    "levels": LevelSitemap,
    "packages": PackageSitemap,
    "legal": LegalSitemap,
}
