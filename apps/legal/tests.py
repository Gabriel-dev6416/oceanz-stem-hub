import pytest
from django.urls import reverse

from .models import SLUGS, LegalPage
from .templatetags.legal_text import legal_body


@pytest.mark.django_db
@pytest.mark.parametrize("slug", [slug for slug, _ in SLUGS])
def test_every_legal_page_is_seeded_as_a_draft(client, slug):
    response = client.get(reverse("legal:page", args=[slug]))

    assert response.status_code == 200
    assert "draft under review" in response.content.decode()


@pytest.mark.django_db
def test_approved_page_hides_the_draft_notice(client):
    LegalPage.objects.filter(slug="terms").update(status=LegalPage.Status.APPROVED)

    html = client.get(reverse("legal:page", args=["terms"])).content.decode()

    assert "draft under review" not in html
    assert "There are no instalments." in html


@pytest.mark.django_db
def test_policies_state_the_srs_rules(client):
    no_refund = client.get(reverse("legal:page", args=["no-refund-policy"])).content.decode()
    safeguarding = client.get(reverse("legal:page", args=["safeguarding"])).content.decode()
    recording = client.get(reverse("legal:page", args=["recording-policy"])).content.decode()

    assert "becomes credit for the next term" in no_refund
    assert "do not message learners under 18 privately" in safeguarding
    assert "deleted after 12 months" in recording


@pytest.mark.django_db
def test_unknown_legal_page_is_404(client):
    assert client.get("/refund-policy/").status_code == 404


def test_legal_body_formats_and_escapes():
    html = legal_body("## Title <b>\nIntro line one\nline two\n\n- first\n- <script>x</script>")

    assert html == (
        "<h2>Title &lt;b&gt;</h2><p>Intro line one line two</p>"
        "<ul><li>first</li><li>&lt;script&gt;x&lt;/script&gt;</li></ul>"
    )
