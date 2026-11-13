import pytest
from django.urls import reverse

from .models import HomePage, SiteSettings
from .templatetags.contact import tel_link, whatsapp_link
from .views import server_error


@pytest.mark.django_db
def test_health_reports_database_and_cache_ok(client):
    response = client.get(reverse("core:health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok", "cache": "ok"}}
    assert "no-cache" in response["Cache-Control"]


def test_health_rejects_post(client):
    response = client.post(reverse("core:health"))

    assert response.status_code == 405


@pytest.mark.django_db
def test_home_shows_hero_and_contacts_from_settings(client):
    response = client.get(reverse("core:home"))

    assert response.status_code == 200
    html = response.content.decode()
    assert "Verified STEM teachers" in html
    assert '<span class="highlight">M.S.C</span>' in html
    assert "https://wa.me/2347064579661?text=" in html
    assert 'href="tel:+2347064579661"' in html
    assert "oceanzstemhub@gmail.com" in html
    for line in ("tel:+2347055260308", "tel:+2349028353019"):
        assert line in html
    assert "#5 Gunning Rd, Abakaliki, Ebonyi State, Nigeria" in html


@pytest.mark.django_db
def test_layout_follows_srs_v3_3(client):
    html = client.get(reverse("core:home")).content.decode()

    assert "img/oceanz-mark.webp" in html
    assert "fonts/manrope-latin-wght-normal.woff2" in html
    for choice in ("light", "dark", "system"):
        assert f'data-theme-choice="{choice}"' in html
    assert 'class="phone-bar"' in html
    assert "We don&#x27;t just raise learners" in html
    assert "Consistency &middot; Competence &middot; Character" in html


@pytest.mark.django_db
def test_footer_shows_only_filled_social_links(client):
    html = client.get(reverse("core:home")).content.decode()
    assert "Follow us" not in html

    site = SiteSettings.load()
    site.instagram_url = "https://instagram.com/oceanzstemhub"
    site.whatsapp_channel_url = "https://whatsapp.com/channel/oceanz"
    site.save()
    html = client.get(reverse("core:home")).content.decode()

    assert 'href="https://instagram.com/oceanzstemhub"' in html
    assert ">WhatsApp channel<" in html
    assert ">Facebook<" not in html


@pytest.mark.django_db
def test_editing_site_settings_updates_pages(client):
    client.get(reverse("core:home"))  # warm the cache
    settings_row = SiteSettings.load()
    settings_row.whatsapp = "+234 800 000 0001"
    settings_row.address = "OCEANZ Hub, Lagos"
    settings_row.save()

    html = client.get(reverse("core:home")).content.decode()

    assert "https://wa.me/2348000000001?text=" in html
    assert "OCEANZ Hub, Lagos" in html


@pytest.mark.django_db
def test_editing_homepage_hero_updates_page(client):
    home = HomePage.load()
    home.hero_title = "Learn STEM with OCEANZ"
    home.hero_highlight = ""
    home.save()

    html = client.get(reverse("core:home")).content.decode()

    assert "Learn STEM with OCEANZ</h1>" in html


@pytest.mark.django_db
def test_singletons_keep_one_row():
    first = SiteSettings.load()
    SiteSettings(email="other@example.com").save()

    assert SiteSettings.objects.count() == 1
    assert first.pk == 1
    assert SiteSettings.load().email == "other@example.com"


@pytest.mark.django_db
def test_security_headers(client):
    response = client.get(reverse("core:home"))

    assert "default-src 'self'" in response["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in response["Content-Security-Policy"]
    assert "camera=()" in response["Permissions-Policy"]
    assert response["X-Frame-Options"] == "DENY"


@pytest.mark.django_db
def test_unknown_page_uses_branded_404(client):
    response = client.get("/no-such-page/")

    assert response.status_code == 404
    html = response.content.decode()
    assert "Page not found" in html
    assert "https://wa.me/2347064579661" in html


def test_server_error_page_works_without_database(rf):
    response = server_error(rf.get("/"))

    assert response.status_code == 500
    html = response.content.decode()
    assert "Something went wrong" in html
    assert "https://wa.me/2347064579661" in html


def test_contact_links():
    assert tel_link("+234 706 457 9661") == "tel:+2347064579661"
    link = whatsapp_link("+234 706 457 9661", "Pricing")
    assert link.startswith("https://wa.me/2347064579661?text=Hello%20OCEANZ%20STEM%20HUB")
    assert "Pricing%20page" in link
