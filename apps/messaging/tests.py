"""Enquiry and contact tests.

Turnstile is verified against Cloudflare's real endpoint using Cloudflare's published test
keys: the default secret always passes and ALWAYS_FAIL_SECRET always fails.
"""

import re

import pytest
from django.core import mail
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.test import override_settings
from django.urls import reverse

from apps.accounts.models import User
from apps.core import turnstile
from apps.core.models import SiteSettings

from .emails import send_reply
from .models import Enquiry, EnquiryReply

DUMMY_TOKEN = "XXXX.DUMMY.TOKEN.XXXX"
ALWAYS_FAIL_SECRET = "2x0000000000000000000000000000000AA"

ENROLMENT = {
    "interest": "enrolment",
    "name": "Ada Obi",
    "phone": "0706 457 9661",
    "email": "ada@example.com",
    "child_class": "jss-2",
    "tutoring_option": "class",
    "delivery_format": "hybrid",
    "message": "",
    "consent": "on",
    turnstile.RESPONSE_FIELD: DUMMY_TOKEN,
}

CONTACT = {
    "name": "Chidi Eze",
    "email": "chidi@example.com",
    "phone": "+234 803 000 0000",
    "enquiry_type": "tertiary",
    "message": "When does the next Web Development cohort start?",
    "consent": "on",
    turnstile.RESPONSE_FIELD: DUMMY_TOKEN,
}


@pytest.mark.django_db
def test_enquiry_page_shows_form_and_turnstile(client):
    html = client.get(reverse("messaging:enquire")).content.decode()

    assert 'data-sitekey="1x00000000000000000000AA"' in html
    assert "SS 1 Commercial" in html
    assert re.search(r'value="enrolment"[^>]*checked', html)


@pytest.mark.django_db
def test_free_trial_link_preselects_trial(client):
    html = client.get(reverse("messaging:enquire") + "?interest=trial").content.decode()

    assert re.search(r'value="free-trial"[^>]*checked', html)


@pytest.mark.django_db
def test_enrolment_enquiry_is_saved_and_acknowledged(client):
    response = client.post(reverse("messaging:enquire"), ENROLMENT)

    assert response.status_code == 302
    assert response["Location"] == reverse("messaging:received")
    enquiry = Enquiry.objects.get()
    assert enquiry.enquiry_type == Enquiry.Type.ENROLMENT
    assert enquiry.child_class == "jss-2"
    assert enquiry.child_level == "Secondary"
    assert enquiry.status == Enquiry.Status.NEW
    assert enquiry.source_page == reverse("messaging:enquire")
    assert re.fullmatch(r"ENQ-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}", enquiry.reference)

    acknowledgement, staff = mail.outbox
    assert acknowledgement.to == ["ada@example.com"]
    assert enquiry.reference in acknowledgement.subject
    assert "JSS 2" in acknowledgement.body
    assert staff.to == [SiteSettings.load().email]
    assert staff.reply_to == ["ada@example.com"]

    received = client.get(response["Location"]).content.decode()
    assert enquiry.reference in received


@pytest.mark.django_db
def test_free_trial_enquiry_is_typed_as_trial(client):
    client.post(reverse("messaging:enquire"), {**ENROLMENT, "interest": "free-trial"})

    assert Enquiry.objects.get().enquiry_type == Enquiry.Type.FREE_TRIAL


@pytest.mark.django_db
def test_enrolment_requires_class_option_format_and_consent(client):
    data = {**ENROLMENT}
    for field in ("child_class", "tutoring_option", "delivery_format", "consent"):
        data.pop(field)

    response = client.post(reverse("messaging:enquire"), data)

    assert response.status_code == 200
    form = response.context["form"]
    assert set(form.errors) == {"child_class", "tutoring_option", "delivery_format", "consent"}
    assert not Enquiry.objects.exists()


@pytest.mark.django_db
@override_settings(TURNSTILE_SECRET_KEY=ALWAYS_FAIL_SECRET)
def test_failed_turnstile_check_blocks_the_enquiry(client):
    response = client.post(reverse("messaging:enquire"), ENROLMENT)

    assert response.status_code == 200
    assert "could not confirm you are human" in response.content.decode()
    assert not Enquiry.objects.exists()
    assert mail.outbox == []


@pytest.mark.django_db
def test_missing_turnstile_token_blocks_the_enquiry(client):
    data = {**ENROLMENT}
    data.pop(turnstile.RESPONSE_FIELD)

    response = client.post(reverse("messaging:enquire"), data)

    assert response.status_code == 200
    assert not Enquiry.objects.exists()


@pytest.mark.django_db
def test_contact_form_saves_chosen_topic(client):
    response = client.post(reverse("messaging:contact"), CONTACT)

    assert response.status_code == 302
    enquiry = Enquiry.objects.get()
    assert enquiry.enquiry_type == Enquiry.Type.TERTIARY
    assert enquiry.message.startswith("When does")
    assert len(mail.outbox) == 2


@pytest.mark.django_db
def test_contact_form_requires_a_message(client):
    response = client.post(reverse("messaging:contact"), {**CONTACT, "message": ""})

    assert "message" in response.context["form"].errors


@pytest.mark.django_db
@override_settings(ENQUIRY_RATE="2/h")
def test_enquiry_posts_are_rate_limited(client):
    for _ in range(2):
        assert client.post(reverse("messaging:contact"), {}).status_code == 200

    response = client.post(reverse("messaging:contact"), {})

    assert response.status_code == 429
    assert "Too many attempts" in response.content.decode()


@pytest.mark.django_db
def test_received_page_without_enquiry_redirects_home(client):
    response = client.get(reverse("messaging:received"))

    assert response.status_code == 302
    assert response["Location"] == reverse("core:home")


@pytest.mark.django_db
def test_contact_page_shows_map_only_with_address(client):
    assert "google.com/maps" not in client.get(reverse("messaging:contact")).content.decode()

    site = SiteSettings.load()
    site.address = "12 Marina Road, Lagos"
    site.save()
    html = client.get(reverse("messaging:contact")).content.decode()

    assert "https://www.google.com/maps?q=12%20Marina%20Road%2C%20Lagos&amp;output=embed" in html


@pytest.mark.django_db
def test_header_links_to_contact_and_enrolment(client):
    html = client.get(reverse("core:home")).content.decode()

    assert f'href="{reverse("messaging:contact")}"' in html
    assert f'href="{reverse("messaging:enquire")}?interest=trial"' in html
    assert 'aria-controls="site-menu"' in html


@pytest.mark.django_db
def test_reply_is_emailed_and_status_updated():
    enquiry = Enquiry.objects.create(
        enquiry_type=Enquiry.Type.ENROLMENT, name="Ada", email="ada@example.com", phone="0706"
    )
    reply = EnquiryReply.objects.create(enquiry=enquiry, body="JSS 2 classes start Monday.")

    assert send_reply(reply)

    reply.refresh_from_db()
    enquiry.refresh_from_db()
    assert reply.sent_at is not None
    assert enquiry.status == Enquiry.Status.AWAITING_REPLY
    assert mail.outbox[0].to == ["ada@example.com"]
    assert "JSS 2 classes start Monday." in mail.outbox[0].body


@pytest.mark.django_db
def test_admin_reply_sends_email(client, settings):
    admin_user = User.objects.create_superuser("owner", "owner@example.com", "x" * 16)
    client.force_login(admin_user)
    enquiry = Enquiry.objects.create(
        enquiry_type=Enquiry.Type.ENROLMENT, name="Ada", email="ada@example.com", phone="0706"
    )
    url = reverse("admin:messaging_enquiry_change", args=[enquiry.pk])
    management = {
        f"{prefix}-{key}": value
        for prefix in ("notes", "replies")
        for key, value in (
            ("TOTAL_FORMS", "1" if prefix == "replies" else "0"),
            ("INITIAL_FORMS", "0"),
            ("MIN_NUM_FORMS", "0"),
            ("MAX_NUM_FORMS", "1000"),
        )
    }

    response = client.post(
        url,
        {
            "status": "in-progress",
            "assigned_to": admin_user.pk,
            **management,
            "replies-0-body": "Thank you. A JSS 2 class place is available.",
            "replies-0-enquiry": enquiry.pk,
        },
    )

    assert response.status_code == 302
    reply = enquiry.replies.get()
    assert reply.author == admin_user
    assert reply.sent_at is not None
    assert mail.outbox[0].to == ["ada@example.com"]
    enquiry.refresh_from_db()
    assert enquiry.assigned_to == admin_user


def test_turnstile_verifies_against_cloudflare(settings):
    assert turnstile.verify(DUMMY_TOKEN)
    settings.TURNSTILE_SECRET_KEY = ALWAYS_FAIL_SECRET
    assert not turnstile.verify(DUMMY_TOKEN)
    assert not turnstile.verify("")


def test_deploy_check_rejects_test_keys_and_console_email(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    with pytest.raises(SystemCheckError) as error:
        call_command("check", "--deploy", "--tag", "security")

    assert "core.E001" in str(error.value)
    assert "core.E002" in str(error.value)
