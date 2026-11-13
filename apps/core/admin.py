from django.contrib import admin

from .models import FAQ, AboutPage, FeatureCard, HomePage, SiteSettings, Stat, Testimonial


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "WhatsApp and call lines",
            {"fields": ("whatsapp", "phone_primary", "phone_secondary", "phone_tertiary")},
        ),
        ("Email and hub", {"fields": ("email", "address", "office_hours", "brand_line")}),
        ("Notice bar", {"fields": ("notice_text", "notice_link", "notice_link_text")}),
        (
            "Fees and bank details",
            {
                "fields": (
                    "registration_fee",
                    "sibling_discount_percent",
                    "bank_name",
                    "bank_account_name",
                    "bank_account_number",
                )
            },
        ),
        (
            "Social media",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "x_url",
                    "youtube_url",
                    "tiktok_url",
                    "linkedin_url",
                    "whatsapp_channel_url",
                )
            },
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(SingletonAdmin):
    fieldsets = (("Hero", {"fields": ("hero_badge", "hero_title", "hero_highlight", "hero_text")}),)


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ("order", "published")


@admin.register(FeatureCard)
class FeatureCardAdmin(OrderedAdmin):
    list_display = ("title", "icon", "order", "published")


@admin.register(Stat)
class StatAdmin(OrderedAdmin):
    list_display = ("value", "label", "order", "published")


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ("question", "order", "published")
    search_fields = ("question", "answer")


@admin.register(Testimonial)
class TestimonialAdmin(OrderedAdmin):
    list_display = ("name", "relation", "consent_confirmed", "order", "published")
    list_editable = ("order",)


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    fields = ("vision", "mission", "story", "founded_year")
