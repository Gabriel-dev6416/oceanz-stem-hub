from decimal import Decimal

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import FAQ, AboutPage, HomePage, SiteSettings, Stat, Testimonial
from .templatetags.contact import tel_link, whatsapp_link
from .templatetags.money import naira
from .templatetags.seo import jsonld
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


@pytest.mark.django_db
def test_homepage_bands_follow_srs_v3_3(client):
    html = client.get(reverse("core:home")).content.decode()

    for text in (
        "Live online classes",
        "Weekly reports to parents",
        "Our core values: C<sup>3</sup>",
        "Who we teach",
        "SS 1 to 3, Science and Art",
        "Computer Hardware and GSM Repairs",
        "Home lessons",
        "Pay the registration fee",
        "A one-time ₦1,000 per child.",
        "A quiet learning space",
        "?interest=international",
        "?interest=private",
    ):
        assert text in html, text


@pytest.mark.django_db
def test_stats_replace_feature_cards_once_published(client):
    assert "Live online classes" in client.get(reverse("core:home")).content.decode()

    Stat.objects.create(value="250+", label="learners taught")
    html = client.get(reverse("core:home")).content.decode()

    assert "<strong>250+</strong>" in html
    assert "Live online classes" not in html


@pytest.mark.django_db
def test_faq_drafts_stay_hidden_until_published(client):
    assert FAQ.objects.filter(published=False).count() == 5
    assert 'id="faq"' not in client.get(reverse("core:home")).content.decode()

    FAQ.objects.filter(question="How much is registration?").update(published=True)
    html = client.get(reverse("core:home")).content.decode()

    assert 'id="faq"' in html
    assert "How much is registration?" in html
    assert "Who can learn at OCEANZ STEM HUB?" not in html


@pytest.mark.django_db
def test_testimonials_need_consent_and_publishing(client):
    item = Testimonial(quote="My son loves coding now.", name="Ngozi", published=True)
    with pytest.raises(ValidationError):
        item.full_clean()

    item.consent_confirmed = True
    item.full_clean()
    item.save()

    assert "My son loves coding now." in client.get(reverse("core:home")).content.decode()


@pytest.mark.django_db
def test_notice_bar_shows_only_when_set(client):
    assert "notice-bar" not in client.get(reverse("core:home")).content.decode()

    site = SiteSettings.load()
    site.notice_text = "Second term registration is open"
    site.notice_link = "/enquire/"
    site.save()
    html = client.get(reverse("messaging:contact")).content.decode()

    assert "Second term registration is open" in html
    assert f'data-notice-id="{site.notice_id}"' in html
    assert 'href="/enquire/"' in html


def test_naira_formatting():
    assert naira(Decimal("1000")) == "₦1,000"
    assert naira(Decimal("40000.00")) == "₦40,000"
    assert naira(Decimal("1500.5")) == "₦1,500.50"


@pytest.mark.django_db
def test_about_page(client):
    html = client.get(reverse("core:about")).content.decode()

    for text in (
        "To raise a generation of knowledgeable learners",
        "To identify, nurture and empower young minds",
        "Consistency",
        "Identify",
        "Empower",
        "#5 Gunning Rd",
    ):
        assert text in html, text
    assert "Our story" not in html.split("<main")[1]

    about = AboutPage.load()
    about.story = "OCEANZ began in Abakaliki.\n\nWe started with coding clubs."
    about.founded_year = 2024
    about.save()
    html = client.get(reverse("core:about")).content.decode()

    assert "<p>We started with coding clubs.</p>" in html
    assert "Founded in 2024" in html


@pytest.mark.django_db
def test_results_page_exists_only_with_published_stats(client):
    assert client.get(reverse("core:results")).status_code == 404
    assert 'href="/results/"' not in client.get(reverse("core:home")).content.decode()

    Stat.objects.create(value="120", label="learners in 2026")

    assert "<strong>120</strong>" in client.get(reverse("core:results")).content.decode()
    assert 'href="/results/"' in client.get(reverse("core:home")).content.decode()


@pytest.mark.django_db
def test_diaspora_page(client):
    html = client.get(reverse("core:diaspora")).content.decode()

    assert "Keep your child on the Nigerian curriculum from anywhere" in html
    assert "Priced by quote, including registration" in html
    assert "?interest=international" in html
    assert "₦" not in html.split("<main")[1].split("</main>")[0]


@pytest.mark.django_db
def test_seo_files(client):
    robots = client.get("/robots.txt").content.decode()
    assert "Sitemap: http://testserver/sitemap.xml" in robots
    assert settings.ADMIN_URL not in robots

    sitemap = client.get("/sitemap.xml").content.decode()
    for path in (
        "/about/",
        "/pricing/",
        "/programmes/junior-secondary/",
        "/programmes/tertiary/web-development/",
        "/privacy/",
        "/teach-with-us/",
    ):
        assert f"<loc>http://testserver{path}</loc>" in sitemap, path

    security = client.get("/.well-known/security.txt").content.decode()
    assert "Contact: mailto:oceanzstemhub@gmail.com" in security
    assert "Expires: " in security


@pytest.mark.django_db
def test_homepage_meta_and_structured_data(client):
    html = client.get(reverse("core:home")).content.decode()

    assert '<link rel="canonical" href="http://testserver/">' in html
    assert 'property="og:title" content="OCEANZ STEM HUB"' in html
    assert '"@type": "EducationalOrganization"' in html
    assert '"FAQPage"' not in html

    FAQ.objects.filter(question="How much is registration?").update(published=True)
    assert '"@type": "FAQPage"' in client.get(reverse("core:home")).content.decode()


def test_structured_data_cannot_break_out_of_the_script():
    tag = jsonld({"name": "</script><script>alert(1)</script>"})

    assert "</script><script>" not in tag
    assert tag.endswith("</script>")
    assert tag.count("</script>") == 1


@pytest.mark.django_db
def test_cookie_notice_and_map_consent(client):
    html = client.get(reverse("messaging:contact")).content.decode()

    assert "data-cookie-notice" in html
    assert "<iframe" not in html
    assert "data-map-src=" in html
    assert "Show the map" in html
