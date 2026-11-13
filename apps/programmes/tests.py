import pytest
from django.urls import reverse

from apps.core.models import SiteSettings

from .classes import level_slug
from .models import CurriculumTopic, Level, TermProject, TertiaryPackage


def page(client, name, *args):
    response = client.get(reverse(name, args=args))
    assert response.status_code == 200
    return response.content.decode()


@pytest.mark.django_db
def test_pricing_shows_srs_v3_3_fees_in_naira(client):
    html = page(client, "programmes:pricing")

    for text in (
        "₦1,000",  # registration
        "Senior Secondary Science</a></th><td>SS 1, 2 and 3, Science stream</td><td>₦40,000",
        "Junior Secondary</a></th><td>JSS 1, 2 and 3</td><td>₦30,000",
        "Easter/April</th><td>Announced before the holiday</td><td>₦40,000",
        "Summer/August</th><td>Announced before the holiday</td><td>₦60,000",
        "December</th><td>Announced before the holiday</td><td>₦20,000",
        "Sibling discount: 10%",
        "2049402355",
        "First Bank of Nigeria",
        "There are no instalments.",
        "Fees are not refundable after payment.",
    ):
        assert text in html, text


@pytest.mark.django_db
def test_quoted_fees_are_never_published(client):
    html = page(client, "programmes:pricing")

    for title in ("Private tutoring", "Tertiary packages", "Families abroad"):
        assert f"<h3>{title}</h3>" in html
    assert html.count("Price: contact the Admin") == 3
    for internal_guide in ("₦60,000 per month", "₦80,000"):
        assert internal_guide not in html
    for slug in ("web-development", "iot-robotics"):
        assert (
            "₦"
            not in page(client, "programmes:package", slug)
            .split("<main")[1]
            .split("Registration")[0]
        )


@pytest.mark.django_db
def test_fee_changes_in_the_admin_show_on_the_site(client):
    Level.objects.filter(slug="junior-secondary").update(term_fee=35000)
    site = SiteSettings.load()
    site.bank_account_number = "0123456789"
    site.save()

    html = page(client, "programmes:pricing")

    assert "₦35,000" in html
    assert "0123456789" in html


@pytest.mark.django_db
def test_programmes_overview(client):
    html = page(client, "programmes:overview")

    for text in (
        "Term Classes Programme",
        "Holiday Tuition",
        "<span>Junior Secondary</span><strong>₦30,000</strong>",
        '<span class="session-name">Summer/August</span><strong>₦60,000</strong>',
        'id="primary"',
        'id="secondary"',
        "Senior Secondary Art",
        "Online, on-site, hybrid or home lessons",
        "A quiet learning space",
        "Pay the registration fee",
    ):
        assert text in html, text


@pytest.mark.django_db
def test_level_page(client):
    html = page(client, "programmes:level", "senior-secondary-science")

    for text in (
        "Physics",
        "Introduction to Robotics and Competitive/Dynamic Programming",
        "WAEC, NECO and JAMB/UTME",
        "₦40,000",
        "Home lessons",
    ):
        assert text in html, text


@pytest.mark.django_db
def test_unpublished_level_and_package_are_hidden(client):
    Level.objects.filter(slug="senior-secondary-art").update(published=False)
    TertiaryPackage.objects.filter(slug="cybersecurity").update(published=False)

    assert client.get(reverse("programmes:level", args=["senior-secondary-art"])).status_code == 404
    assert client.get(reverse("programmes:package", args=["cybersecurity"])).status_code == 404
    assert "Senior Secondary Art" not in page(client, "programmes:pricing")


@pytest.mark.django_db
def test_tertiary_packages(client):
    html = page(client, "programmes:tertiary")

    assert html.count('class="card package-card"') == 12
    assert "within 4 working days" in html
    assert "Laplace transform" in page(client, "programmes:package", "mathematics-and-statistics")


@pytest.mark.django_db
def test_holiday_tuition_page(client):
    html = page(client, "programmes:holiday")

    assert "SSCE (WAEC and NECO)" in html
    assert "₦60,000" in html


@pytest.mark.django_db
def test_subjects_page_shows_the_stem_pathway(client):
    html = page(client, "programmes:subjects")

    for text in (
        "Unplugged coding, Scratch Jr",
        "Python basics, Arduino introduction",
        "Introduction to Robotics (Science stream)",
        "Laplace transform",
        "Basic Science",
    ):
        assert text in html, text


@pytest.mark.django_db
def test_explorer_without_topics_shows_subjects_and_skills(client):
    html = client.get(
        reverse("programmes:explorer"), {"class_code": "primary-2", "term": 1}
    ).content.decode()

    assert "Primary 2, First term" in html
    assert "The weekly topics for Primary 2 are being prepared" in html
    assert "ScratchJr and Scratch 3" in html
    assert "Numbers, shapes, measurement" in html


@pytest.mark.django_db
def test_explorer_lists_topics_and_project(client):
    CurriculumTopic.objects.create(
        class_code="jss-2", subject="Mathematics", term=2, week=3, title="Linear equations"
    )
    CurriculumTopic.objects.create(
        class_code="jss-2", subject="Mathematics", term=2, week=1, title="Number bases"
    )
    CurriculumTopic.objects.create(
        class_code="jss-2", subject="Mathematics", term=1, week=1, title="Whole numbers"
    )
    TermProject.objects.create(class_code="jss-2", term=2, title="Build a rain gauge")

    html = client.get(
        reverse("programmes:explorer"), {"class_code": "jss-2", "term": 2}
    ).content.decode()

    assert html.index("Number bases") < html.index("Linear equations")
    assert "Whole numbers" not in html
    assert "Termly project: Build a rain gauge" in html
    assert "being prepared" not in html


@pytest.mark.django_db
def test_explorer_rejects_unknown_class(client):
    html = client.get(
        reverse("programmes:explorer"), {"class_code": "tertiary", "term": 1}
    ).content.decode()

    assert "explorer-result" not in html


def test_class_to_level_mapping():
    assert level_slug("primary-3") == "lower-primary"
    assert level_slug("primary-4") == "upper-primary"
    assert level_slug("jss-1") == "junior-secondary"
    assert level_slug("ss-2-science") == "senior-secondary-science"
    assert level_slug("ss-3-art") == "senior-secondary-art"


@pytest.mark.django_db
def test_menu_and_homepage_link_the_new_pages(client):
    html = page(client, "core:home")

    for url in (
        reverse("programmes:overview"),
        reverse("programmes:pricing"),
        reverse("programmes:holiday"),
        reverse("programmes:tertiary"),
        reverse("programmes:subjects"),
        reverse("programmes:explorer"),
        reverse("programmes:package", args=["web-development"]),
    ):
        assert f'href="{url}' in html or f'action="{url}"' in html, url
    assert 'name="class_code"' in html
    assert "<strong>₦30,000</strong><span>Term Classes, per term</span>" in html
    assert '<span class="session-badge">DEC</span>' in html
