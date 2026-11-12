from django.contrib import admin

from .models import HomePage, SiteSettings


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        (
            "WhatsApp and phone",
            {
                "fields": (
                    "whatsapp_primary",
                    "whatsapp_secondary",
                    "phone_primary",
                    "phone_secondary",
                )
            },
        ),
        ("Email and hub", {"fields": ("email", "address", "office_hours")}),
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
                )
            },
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(SingletonAdmin):
    fieldsets = (("Hero", {"fields": ("hero_badge", "hero_title", "hero_highlight", "hero_text")}),)
