import hashlib
from decimal import Decimal

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    r"^\+\d[\d ]{7,18}$",
    "Use international format, for example +234 706 457 9661.",
)


DEFAULT_ADDRESS = "#5 Gunning Rd, Abakaliki, Ebonyi State, Nigeria"


class SingletonModel(models.Model):
    """A model with exactly one row (pk=1), cached and edited from the back-office."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self._cache_key())

    @classmethod
    def _cache_key(cls):
        return f"singleton:{cls._meta.label_lower}"

    @classmethod
    def load(cls):
        obj = cache.get(cls._cache_key())
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set(cls._cache_key(), obj, timeout=3600)
        return obj


class SiteSettings(SingletonModel):
    """Contact details and links shown on every public page (FR-WEB-10, FR-WEB-20, FR-COM-03)."""

    whatsapp = models.CharField(
        "WhatsApp number", max_length=20, default="+234 706 457 9661", validators=[phone_validator]
    )
    phone_primary = models.CharField(
        "call line 1", max_length=20, default="+234 706 457 9661", validators=[phone_validator]
    )
    phone_secondary = models.CharField(
        "call line 2",
        max_length=20,
        blank=True,
        default="+234 705 526 0308",
        validators=[phone_validator],
    )
    phone_tertiary = models.CharField(
        "call line 3",
        max_length=20,
        blank=True,
        default="+234 902 835 3019",
        validators=[phone_validator],
    )
    email = models.EmailField(default="oceanzstemhub@gmail.com")
    address = models.TextField("hub address", blank=True, default=DEFAULT_ADDRESS)
    office_hours = models.CharField(max_length=120, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    x_url = models.URLField("X (Twitter) URL", blank=True)
    youtube_url = models.URLField(blank=True)
    tiktok_url = models.URLField("TikTok URL", blank=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True)
    whatsapp_channel_url = models.URLField("WhatsApp channel URL", blank=True)
    registration_fee = models.DecimalField(
        "registration fee (naira)",
        max_digits=10,
        decimal_places=2,
        default=Decimal("1000"),
        help_text="One-time, non-refundable fee per child (FR-PAY-01).",
    )
    sibling_discount_percent = models.PositiveSmallIntegerField(
        "sibling discount (%)",
        default=10,
        help_text="On programme fees for the second and further children (FR-PAY-02).",
    )
    bank_name = models.CharField(max_length=80, default="First Bank of Nigeria")
    bank_account_name = models.CharField(max_length=80, default="OCEANZ STEM HUB")
    bank_account_number = models.CharField(max_length=20, default="2049402355")
    notice_text = models.CharField(
        max_length=160,
        blank=True,
        help_text="Shown in a bar above the header on every page. Leave empty to hide it.",
    )
    notice_link = models.CharField(
        max_length=200, blank=True, help_text="Optional page address, e.g. /enquire/"
    )
    notice_link_text = models.CharField(max_length=40, blank=True, default="Learn more")
    brand_line = models.CharField(
        max_length=160,
        default="We don't just raise learners; we raise teachers, professionals, innovators "
        "and leaders.",
    )

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    @property
    def notice_id(self):
        """Changes whenever the notice text changes, so a new notice shows again."""
        return hashlib.sha256(self.notice_text.encode()).hexdigest()[:12]

    @property
    def call_lines(self):
        return [n for n in (self.phone_primary, self.phone_secondary, self.phone_tertiary) if n]

    @property
    def social_links(self):
        links = [
            ("Facebook", self.facebook_url),
            ("Instagram", self.instagram_url),
            ("X", self.x_url),
            ("YouTube", self.youtube_url),
            ("TikTok", self.tiktok_url),
            ("LinkedIn", self.linkedin_url),
            ("WhatsApp channel", self.whatsapp_channel_url),
        ]
        return [(name, url) for name, url in links if url]


class HomePage(SingletonModel):
    """Editable homepage content (FR-WEB-08). Further blocks are added with each section."""

    hero_badge = models.CharField(
        max_length=120, default="Verified STEM teachers · Primary to Tertiary"
    )
    hero_title = models.CharField(max_length=80, default="STEM Education")
    hero_highlight = models.CharField(
        max_length=40, blank=True, default="M.S.C", help_text="Shown in gold after the title."
    )
    hero_text = models.TextField(
        default=(
            "Mathematics, Science and Coding/Digital Technologies for Primary, Secondary and "
            "Tertiary learners in Nigeria and abroad. Live lessons online, on-site every "
            "Saturday, or both."
        )
    )

    class Meta:
        verbose_name = "homepage"
        verbose_name_plural = "homepage"

    def __str__(self):
        return "Homepage"


class OrderedItem(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class FeatureCard(OrderedItem):
    """Trust-strip cards on the homepage (FR-WEB-01 band 3)."""

    class Icon(models.TextChoices):
        LIVE = "live", "Live class"
        ON_SITE = "on-site", "Calendar (on-site Saturdays)"
        VERIFIED = "verified", "Shield (verified teachers)"
        REPORTS = "reports", "Document (reports)"

    title = models.CharField(max_length=60)
    text = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, choices=Icon.choices)

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return self.title


class Stat(OrderedItem):
    """A real, verifiable figure (FR-WEB-06). The stats bar replaces the feature cards once one
    is published."""

    value = models.CharField(max_length=20, help_text="For example 250+ or 98%.")
    label = models.CharField(max_length=80)

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return f"{self.value} {self.label}"


class FAQ(OrderedItem):
    """Frequently asked question. Only published questions appear on the site."""

    question = models.CharField(max_length=200)
    answer = models.TextField()
    published = models.BooleanField(default=False)

    class Meta(OrderedItem.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Testimonial(OrderedItem):
    """Genuine, consented and approved testimonial (FR-WEB-11)."""

    quote = models.TextField()
    name = models.CharField(
        max_length=60, help_text="First name only for anyone under 18 (FR-SAF-05)."
    )
    relation = models.CharField(max_length=80, blank=True, help_text="e.g. Parent, JSS 2")
    consent_confirmed = models.BooleanField(
        default=False, help_text="The person agreed in writing to this testimonial being shown."
    )
    published = models.BooleanField(default=False)

    class Meta(OrderedItem.Meta):
        pass

    def __str__(self):
        return f"{self.name}: {self.quote[:40]}"

    def clean(self):
        if self.published and not self.consent_confirmed:
            raise ValidationError({"published": "Confirm consent before publishing."})


class AboutPage(SingletonModel):
    """About page content (FR-WEB-07). The story section shows only once it is written."""

    vision = models.TextField(
        default=(
            "To raise a generation of knowledgeable learners, confident educators and competent "
            "professionals who will thrive, innovate and lead in a world driven by Artificial "
            "Intelligence, Science and Technology."
        )
    )
    mission = models.TextField(
        default=(
            "To identify, nurture and empower young minds by equipping them with relevant "
            "knowledge, practical skills, professional competence and strong character, "
            "inspiring them to discover their potential, develop their gifts and become leaders "
            "in their chosen fields."
        )
    )
    story = models.TextField(
        "our story",
        blank=True,
        help_text="The OCEANZ story, the meaning of the name and facts about the team. "
        "Separate paragraphs with a blank line. Hidden while empty.",
    )
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "about page"
        verbose_name_plural = "about page"

    def __str__(self):
        return "About page"
