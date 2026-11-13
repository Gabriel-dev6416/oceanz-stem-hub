from django.db import models
from django.urls import reverse

SLUGS = [
    ("privacy", "Privacy Policy"),
    ("terms", "Terms of Service"),
    ("no-refund-policy", "No-Refund Policy"),
    ("safeguarding", "Child Protection and Safeguarding Policy"),
    ("academic-integrity", "Academic Integrity Policy"),
    ("cookie-policy", "Cookie Policy"),
    ("recording-policy", "Recording Policy"),
]


class LegalPage(models.Model):
    """A legal page (FR-WEB-09). Body: blank lines separate paragraphs, '## ' starts a heading
    and '- ' starts a list item."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft (shows an 'under review' notice)"
        APPROVED = "approved", "Approved"

    slug = models.SlugField(unique=True, choices=SLUGS)
    title = models.CharField(max_length=80)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    version = models.CharField(max_length=20, default="0.1")
    effective_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("legal:page", args=[self.slug])
