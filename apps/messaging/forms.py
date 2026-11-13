from django import forms
from django.conf import settings

from apps.core import turnstile

from .models import Enquiry

NIGERIA = "Nigeria"
CONSENT_LABEL = "OCEANZ STEM HUB may contact me by phone, WhatsApp or email about this enquiry."


class TurnstileForm(forms.ModelForm):
    """Adds Cloudflare Turnstile verification (SEC-ABU-02) and contact consent."""

    consent = forms.BooleanField(label=CONSENT_LABEL)

    def __init__(self, *args, request, **kwargs):
        self.request = request
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        for name, autocomplete in (("name", "name"), ("email", "email"), ("phone", "tel")):
            self.fields[name].widget.attrs["autocomplete"] = autocomplete

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            token = self.data.get(turnstile.RESPONSE_FIELD)
            remote_ip = self.request.META.get(settings.RATELIMIT_IP_META_KEY)
            if not turnstile.verify(token, remote_ip):
                raise forms.ValidationError(
                    "We could not confirm you are human. Please complete the check and try "
                    "again, or contact us on WhatsApp.",
                    code="turnstile",
                )
        return cleaned_data


class EnrolmentEnquiryForm(TurnstileForm):
    """Public enrolment enquiry for visitors not ready to register (FR-WEB-13)."""

    interest = forms.ChoiceField(
        label="I would like to",
        choices=[
            (Enquiry.Type.ENROLMENT, "Enrol my child"),
            (Enquiry.Type.FREE_TRIAL, "Book a free trial class"),
            (Enquiry.Type.PRIVATE_TUTORING, "Get a private tutoring quote"),
            (Enquiry.Type.TERTIARY, "Ask about a tertiary package"),
            (Enquiry.Type.INTERNATIONAL, "Enrol from outside Nigeria (international family)"),
        ],
        widget=forms.RadioSelect,
    )

    field_order = ["interest"]

    class Meta:
        model = Enquiry
        fields = [
            "name",
            "phone",
            "whatsapp",
            "email",
            "country",
            "child_class",
            "tutoring_option",
            "delivery_format",
            "message",
        ]
        labels = {
            "name": "Your name (parent, guardian or adult learner)",
            "whatsapp": "WhatsApp number (if different)",
            "child_class": "Class",
            "tutoring_option": "Tutoring option",
            "delivery_format": "Delivery format",
            "message": "Anything else we should know? (optional)",
        }
        widgets = {
            "tutoring_option": forms.RadioSelect,
            "delivery_format": forms.RadioSelect,
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("country", "child_class", "tutoring_option", "delivery_format"):
            self.fields[name].required = True
        self.fields["country"].initial = NIGERIA
        self.fields["child_class"].choices = [("", "Select a class")] + [
            choice for choice in self.fields["child_class"].choices if choice[0]
        ]
        self.fields["tutoring_option"].choices = Enquiry.TutoringOption.choices
        self.fields["delivery_format"].choices = Enquiry.DeliveryFormat.choices

    def clean(self):
        cleaned_data = super().clean()
        abroad = cleaned_data.get("country", NIGERIA).strip().lower() != NIGERIA.lower()
        if cleaned_data.get("interest") == Enquiry.Type.INTERNATIONAL and not abroad:
            self.add_error("country", "Enter the country you live in outside Nigeria.")
        return cleaned_data

    def save(self, commit=True):
        interest = self.cleaned_data["interest"]
        abroad = self.cleaned_data["country"].strip().lower() != NIGERIA.lower()
        if abroad and interest == Enquiry.Type.ENROLMENT:
            # Families abroad are quoted by the Admin, never shown a price (FR-PAY-13).
            interest = Enquiry.Type.INTERNATIONAL
        self.instance.enquiry_type = interest
        return super().save(commit)


class ContactForm(TurnstileForm):
    """General contact form (FR-COM-01)."""

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "enquiry_type", "message"]
        labels = {"phone": "Phone or WhatsApp number", "enquiry_type": "What is it about?"}
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].required = True
        self.fields["enquiry_type"].choices = [("", "Select a topic")] + list(Enquiry.Type.choices)
