from django import forms

from apps.core.forms import TurnstileForm

from .models import TeacherInterest


class InterestForm(TurnstileForm):
    consent_label = (
        "OCEANZ STEM HUB may store these details and contact me about teaching opportunities."
    )

    subjects = forms.MultipleChoiceField(
        label="Subjects you can teach",
        choices=TeacherInterest.Subject.choices,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = TeacherInterest
        fields = ["name", "email", "whatsapp", "subjects"]
