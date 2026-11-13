import secrets

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

REFERENCE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O or 1/I to avoid misreading

visitor_phone_validator = RegexValidator(
    r"^\+?\d[\d \-]{6,18}$",
    "Enter a phone number, for example 0706 457 9661 or +234 706 457 9661.",
)

# Classes from the Nigerian school system (SRS 3.1). Primary 1-3 are listed separately for
# parents and form the Junior Primary class. R2 replaces this list with the Admin-managed classes.
CLASS_CHOICES = [
    (
        "Primary",
        [(f"primary-{year}", f"Primary {year}") for year in range(1, 7)],
    ),
    (
        "Secondary",
        [
            ("jss-1", "JSS 1"),
            ("jss-2", "JSS 2"),
            ("jss-3", "JSS 3"),
            ("ss-1-science", "SS 1 Science"),
            ("ss-1-art", "SS 1 Art"),
            ("ss-2-science", "SS 2 Science"),
            ("ss-2-art", "SS 2 Art"),
            ("ss-3-science", "SS 3 Science"),
            ("ss-3-art", "SS 3 Art"),
        ],
    ),
    ("Tertiary", [("tertiary", "Tertiary package")]),
]
CLASS_LEVELS = {value: level for level, options in CLASS_CHOICES for value, _ in options}


def new_reference():
    code = "".join(secrets.choice(REFERENCE_ALPHABET) for _ in range(8))
    return f"ENQ-{code[:4]}-{code[4:]}"


class Enquiry(models.Model):
    """A public enrolment enquiry or contact message (FR-WEB-13, FR-COM-01, FR-COM-02)."""

    class Type(models.TextChoices):
        ENROLMENT = "enrolment", "Enrolment"
        FREE_TRIAL = "free-trial", "Free trial class"
        PRIVATE_TUTORING = "private-tutoring", "Private tutoring"
        TERTIARY = "tertiary", "Tertiary packages"
        HOLIDAY = "holiday", "Holiday Tuition"
        INTERNATIONAL = "international", "International families"
        FEES = "fees", "Fees and payments"
        TEACH = "teach", "Teach with us"
        TECHNICAL = "technical", "Technical support"
        PARTNERSHIP = "partnership", "Partnership"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in-progress", "In progress"
        AWAITING_REPLY = "awaiting-reply", "Awaiting reply"
        CONVERTED = "converted", "Converted to enrolment"
        CLOSED = "closed", "Closed"

    class TutoringOption(models.TextChoices):
        CLASS = "class", "Class place (with a small group of 6-12)"
        PRIVATE = "private", "Private (one-on-one, priced by quote)"

    class DeliveryFormat(models.TextChoices):
        ONLINE = "online", "Online"
        ON_SITE = "on-site", "On-site at the hub"
        HYBRID = "hybrid", "Hybrid (online weekdays, on-site Saturdays)"
        HOME = "home", "Home lessons (after school and weekends, Abakaliki area)"

    reference = models.CharField(max_length=13, unique=True, editable=False)
    enquiry_type = models.CharField(max_length=20, choices=Type.choices)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=24, validators=[visitor_phone_validator])
    whatsapp = models.CharField(
        "WhatsApp number", max_length=24, blank=True, validators=[visitor_phone_validator]
    )
    country = models.CharField("country of residence", max_length=60, blank=True)
    child_class = models.CharField(
        "child's class", max_length=20, blank=True, choices=CLASS_CHOICES
    )
    tutoring_option = models.CharField(max_length=10, blank=True, choices=TutoringOption.choices)
    delivery_format = models.CharField(max_length=10, blank=True, choices=DeliveryFormat.choices)
    message = models.TextField(blank=True)
    source_page = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_enquiries",
        limit_choices_to={"is_staff": True},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"
        indexes = [models.Index(fields=["status", "-created_at"])]

    def __str__(self):
        return f"{self.reference} {self.name}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = new_reference()
            while Enquiry.objects.filter(reference=self.reference).exists():
                self.reference = new_reference()
        super().save(*args, **kwargs)

    @property
    def child_level(self):
        return CLASS_LEVELS.get(self.child_class, "")


class EnquiryNote(models.Model):
    """Internal note by staff. Never shown to the enquirer."""

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Note on {self.enquiry.reference}"


class EnquiryReply(models.Model):
    """Email reply sent to the enquirer from the back-office."""

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False
    )
    body = models.TextField("reply")
    sent_at = models.DateTimeField(null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "replies"

    def __str__(self):
        return f"Reply to {self.enquiry.reference}"
