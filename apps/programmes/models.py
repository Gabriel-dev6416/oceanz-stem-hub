from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from apps.core.models import OrderedItem

from .classes import SCHOOL_CLASS_CHOICES


class PathwayStage(OrderedItem):
    """One row of the OCEANZ STEM pathway (SRS 3.4): what each subject covers at a stage."""

    name = models.CharField(max_length=40)
    mathematics = models.TextField()
    science = models.TextField()
    coding = models.TextField("coding / digital technologies")
    hardware = models.TextField("hardware, robotics and engineering")

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return self.name


class Level(OrderedItem):
    """A school level with its own programme page and Term Classes fee (FR-WEB-03, FR-PAY-01)."""

    class Group(models.TextChoices):
        PRIMARY = "primary", "Primary"
        SECONDARY = "secondary", "Secondary"

    group = models.CharField(max_length=10, choices=Group.choices)
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    classes = models.CharField(max_length=80, help_text="e.g. JSS 1, 2 and 3")
    ages = models.CharField("typical ages", max_length=20)
    exams = models.CharField("exam preparation", max_length=120, blank=True)
    stage = models.ForeignKey(PathwayStage, on_delete=models.PROTECT, related_name="levels")
    term_fee = models.DecimalField(
        "Term Classes Programme fee per term (naira)", max_digits=10, decimal_places=2
    )

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("programmes:level", args=[self.slug])


class LevelSubject(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=80)
    detail = models.CharField(max_length=160, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class HolidaySession(OrderedItem):
    """A Holiday Tuition session (SRS 3.6, FR-ACD-07)."""

    name = models.CharField(max_length=40, help_text="e.g. Easter/April")
    fee = models.DecimalField("fee per session (naira)", max_digits=10, decimal_places=2)
    dates = models.CharField(max_length=80, blank=True, help_text="Shown when set.")

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return self.name

    @property
    def badge(self):
        """Short month label for the session tile, e.g. 'Easter/April' -> 'APR'."""
        return self.name.split("/")[-1].strip()[:3].upper()


class TertiaryPackage(OrderedItem):
    """A tertiary package (SRS 3.5). Fees are quoted by the Admin and never published."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    focus = models.CharField(max_length=200)
    delivery = models.CharField(max_length=80)

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("programmes:package", args=[self.slug])


class Term(models.IntegerChoices):
    FIRST = 1, "First term"
    SECOND = 2, "Second term"
    THIRD = 3, "Third term"


class CurriculumTopic(models.Model):
    """Weekly topic for a class, subject and term (FR-ACD-05, decision D-01)."""

    class_code = models.CharField("class", max_length=20, choices=SCHOOL_CLASS_CHOICES)
    subject = models.CharField(max_length=80)
    term = models.PositiveSmallIntegerField(choices=Term.choices)
    week = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(13)]
    )
    title = models.CharField(max_length=160)
    objectives = models.TextField(blank=True)

    class Meta:
        ordering = ["class_code", "term", "subject", "week"]
        indexes = [models.Index(fields=["class_code", "term"])]

    def __str__(self):
        return f"{self.get_class_code_display()} {self.subject} T{self.term} W{self.week}"


class TermProject(models.Model):
    """The termly STEM project for a class (FR-ENG-01)."""

    class_code = models.CharField("class", max_length=20, choices=SCHOOL_CLASS_CHOICES)
    term = models.PositiveSmallIntegerField(choices=Term.choices)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["class_code", "term"]
        constraints = [
            models.UniqueConstraint(fields=["class_code", "term"], name="one_project_per_term")
        ]

    def __str__(self):
        return f"{self.get_class_code_display()} {self.get_term_display()}: {self.title}"
