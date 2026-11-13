from django.db import models

from apps.messaging.models import visitor_phone_validator


class TeacherInterest(models.Model):
    """'Express interest' from the Teach with us page (FR-WEB-15, R1). In R2 these people are
    invited to the full application (FR-REC-07)."""

    class Subject(models.TextChoices):
        MATHEMATICS = "mathematics", "Mathematics"
        SCIENCE = "science", "Science (Basic Science, Physics, Chemistry, Biology)"
        CODING = "coding", "Coding/Digital Technologies"
        HARDWARE = "hardware", "Computer Hardware and GSM Repairs"
        ROBOTICS = "robotics", "Robotics and IoT"
        TERTIARY = "tertiary", "Tertiary digital skills packages"

    class Status(models.TextChoices):
        NEW = "new", "New"
        INVITED = "invited", "Invited to apply"
        NOT_SUITABLE = "not-suitable", "Not suitable"

    name = models.CharField("full name", max_length=120)
    email = models.EmailField()
    whatsapp = models.CharField(
        "WhatsApp number", max_length=24, validators=[visitor_phone_validator]
    )
    subjects = models.JSONField(default=list)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEW)
    notes = models.TextField("internal notes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "expression of interest"
        verbose_name_plural = "expressions of interest"

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def subject_names(self):
        labels = dict(self.Subject.choices)
        return [labels.get(value, value) for value in self.subjects]
