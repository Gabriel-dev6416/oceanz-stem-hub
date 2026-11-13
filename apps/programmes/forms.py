from django import forms

from .classes import SCHOOL_CLASS_CHOICES
from .models import Term


class ExplorerForm(forms.Form):
    """Class and term picker for 'See what your child will learn' (FR-ENG-01)."""

    class_code = forms.ChoiceField(
        label="Class", choices=[("", "Select a class"), *SCHOOL_CLASS_CHOICES]
    )
    term = forms.TypedChoiceField(
        label="Term", choices=Term.choices, coerce=int, initial=Term.FIRST
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_id", "explorer-%s")
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
