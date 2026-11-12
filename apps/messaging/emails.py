import logging
from smtplib import SMTPException

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from apps.core.models import SiteSettings

from .models import Enquiry

logger = logging.getLogger(__name__)


def _send(subject, template, context, to, reply_to=None):
    message = EmailMessage(
        subject=subject,
        body=render_to_string(template, context),
        to=to,
        reply_to=reply_to,
    )
    try:
        message.send()
    except (SMTPException, OSError):
        logger.exception("Email %r to %s failed", subject, to)
        return False
    return True


def send_acknowledgement(enquiry):
    """Confirms receipt to the enquirer with the reference number (FR-COM-01)."""
    site = SiteSettings.load()
    return _send(
        f"We received your enquiry {enquiry.reference}",
        "messaging/email/acknowledgement.txt",
        {"enquiry": enquiry, "site": site},
        to=[enquiry.email],
        reply_to=[site.email],
    )


def notify_staff(enquiry):
    """Tells the OCEANZ inbox about a new enquiry."""
    site = SiteSettings.load()
    return _send(
        f"New enquiry {enquiry.reference}: {enquiry.get_enquiry_type_display()}",
        "messaging/email/staff_notification.txt",
        {"enquiry": enquiry},
        to=[site.email],
        reply_to=[enquiry.email],
    )


def send_reply(reply):
    """Emails a back-office reply to the enquirer and records when it was sent."""
    enquiry = reply.enquiry
    site = SiteSettings.load()
    sent = _send(
        f"Re: your enquiry {enquiry.reference}",
        "messaging/email/reply.txt",
        {"enquiry": enquiry, "reply": reply, "site": site},
        to=[enquiry.email],
        reply_to=[site.email],
    )
    if sent:
        reply.sent_at = timezone.now()
        reply.save(update_fields=["sent_at"])
        if enquiry.status in (Enquiry.Status.NEW, Enquiry.Status.IN_PROGRESS):
            enquiry.status = Enquiry.Status.AWAITING_REPLY
            enquiry.save(update_fields=["status", "updated_at"])
    return sent
