from django.conf import settings
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from apps.core.models import SiteSettings
from apps.messaging.emails import send_email

from .forms import InterestForm

SESSION_KEY = "teacher_interest_name"


def _rate(group, request):
    return settings.ENQUIRY_RATE


@ratelimit(key="ip", rate=_rate, method="POST", block=False)
def teach_with_us(request):
    """Information page and Express interest form (FR-WEB-15, R1)."""
    if getattr(request, "limited", False):
        return render(request, "429.html", status=429)
    form = InterestForm(request.POST or None, request=request)
    if request.method == "POST" and form.is_valid():
        interest = form.save()
        site = SiteSettings.load()
        send_email(
            "Thank you for your interest in teaching with OCEANZ STEM HUB",
            "recruitment/email/acknowledgement.txt",
            {"interest": interest, "site": site},
            to=[interest.email],
            reply_to=[site.email],
        )
        send_email(
            f"New teacher interest: {interest.name}",
            "recruitment/email/staff_notification.txt",
            {"interest": interest},
            to=[site.email],
            reply_to=[interest.email],
        )
        request.session[SESSION_KEY] = interest.name
        return redirect("recruitment:thanks")
    return render(
        request, "recruitment/teach_with_us.html", {"page_title": "Teach with us", "form": form}
    )


def thanks(request):
    name = request.session.get(SESSION_KEY)
    if not name:
        return redirect("recruitment:teach_with_us")
    return render(request, "recruitment/thanks.html", {"page_title": "Teach with us", "name": name})
