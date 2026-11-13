from django import forms
from django.conf import settings

from . import turnstile

AUTOCOMPLETE = {"name": "name", "email": "email", "phone": "tel", "whatsapp": "tel"}


class TurnstileForm(forms.ModelForm):
    """Public form with Cloudflare Turnstile verification (SEC-ABU-02) and contact consent."""

    consent_label = "OCEANZ STEM HUB may contact me by phone, WhatsApp or email about this."

    def __init__(self, *args, request, **kwargs):
        self.request = request
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        self.fields["consent"] = forms.BooleanField(label=self.consent_label)
        for name, value in AUTOCOMPLETE.items():
            if name in self.fields:
                self.fields[name].widget.attrs["autocomplete"] = value

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
