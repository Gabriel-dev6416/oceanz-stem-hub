import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from apps.core import turnstile
from apps.core.models import SiteSettings

from .models import TeacherInterest

DUMMY_TOKEN = "XXXX.DUMMY.TOKEN.XXXX"
ALWAYS_FAIL_SECRET = "2x0000000000000000000000000000000AA"

INTEREST = {
    "name": "Amaka Okafor",
    "email": "amaka@example.com",
    "whatsapp": "0803 000 0000",
    "subjects": ["mathematics", "coding"],
    "consent": "on",
    turnstile.RESPONSE_FIELD: DUMMY_TOKEN,
}


@pytest.mark.django_db
def test_teach_with_us_page(client):
    html = client.get(reverse("recruitment:teach_with_us")).content.decode()

    for text in (
        "Learn a skill and teach to earn",
        "2 to 3 minute introduction video",
        "15-minute demonstration lesson",
        "Safeguarding statement",
        "Consistency, Competence and Character",
        'name="subjects"',
        'data-sitekey="1x00000000000000000000AA"',
    ):
        assert text in html, text


@pytest.mark.django_db
def test_expression_of_interest_is_saved_and_acknowledged(client):
    response = client.post(reverse("recruitment:teach_with_us"), INTEREST)

    assert response.status_code == 302
    assert response["Location"] == reverse("recruitment:thanks")
    interest = TeacherInterest.objects.get()
    assert interest.subjects == ["mathematics", "coding"]
    assert interest.status == TeacherInterest.Status.NEW
    acknowledgement, staff = mail.outbox
    assert acknowledgement.to == ["amaka@example.com"]
    assert "Mathematics, Coding/Digital Technologies" in acknowledgement.body
    assert staff.to == [SiteSettings.load().email]
    assert "Thank you, Amaka Okafor" in client.get(response["Location"]).content.decode()


@pytest.mark.django_db
def test_interest_requires_subjects_and_consent(client):
    data = {**INTEREST}
    data.pop("subjects")
    data.pop("consent")

    response = client.post(reverse("recruitment:teach_with_us"), data)

    assert set(response.context["form"].errors) == {"subjects", "consent"}
    assert not TeacherInterest.objects.exists()


@pytest.mark.django_db
@override_settings(TURNSTILE_SECRET_KEY=ALWAYS_FAIL_SECRET)
def test_interest_needs_turnstile(client):
    client.post(reverse("recruitment:teach_with_us"), INTEREST)

    assert not TeacherInterest.objects.exists()
    assert mail.outbox == []


@pytest.mark.django_db
@override_settings(ENQUIRY_RATE="1/h")
def test_interest_posts_are_rate_limited(client):
    client.post(reverse("recruitment:teach_with_us"), {})

    assert client.post(reverse("recruitment:teach_with_us"), {}).status_code == 429


@pytest.mark.django_db
def test_thanks_page_needs_a_submission(client):
    response = client.get(reverse("recruitment:thanks"))

    assert response["Location"] == reverse("recruitment:teach_with_us")
