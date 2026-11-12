from django.conf import settings
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .emails import notify_staff, send_acknowledgement
from .forms import ContactForm, EnrolmentEnquiryForm
from .models import Enquiry

SESSION_KEY = "enquiry_reference"


def _rate(group, request):
    return settings.ENQUIRY_RATE


def _handle(request, form_class, template, context, initial=None):
    if getattr(request, "limited", False):
        return render(request, "429.html", status=429)
    if request.method == "POST":
        form = form_class(request.POST, request=request)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.source_page = request.path
            enquiry.save()
            send_acknowledgement(enquiry)
            notify_staff(enquiry)
            request.session[SESSION_KEY] = enquiry.reference
            return redirect("messaging:received")
    else:
        form = form_class(request=request, initial=initial)
    return render(request, template, {**context, "form": form})


@ratelimit(key="ip", rate=_rate, method="POST", block=False)
def enquire(request):
    trial = request.GET.get("interest") == "trial"
    interest = Enquiry.Type.FREE_TRIAL if trial else Enquiry.Type.ENROLMENT
    return _handle(
        request,
        EnrolmentEnquiryForm,
        "messaging/enquire.html",
        {"page_title": "Enrol or book a free trial"},
        initial={"interest": interest},
    )


@ratelimit(key="ip", rate=_rate, method="POST", block=False)
def contact(request):
    return _handle(request, ContactForm, "messaging/contact.html", {"page_title": "Contact us"})


def received(request):
    reference = request.session.get(SESSION_KEY)
    if not reference:
        return redirect("core:home")
    return render(
        request,
        "messaging/received.html",
        {"page_title": "Enquiry received", "reference": reference},
    )
