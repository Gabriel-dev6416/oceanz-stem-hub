from django.core.cache import cache
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
