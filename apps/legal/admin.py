from django.contrib import admin

from .models import LegalPage


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "version", "effective_date", "updated_at")
    list_editable = ("status",)
    readonly_fields = ("slug", "updated_at")
    fields = (
        "slug",
        "title",
        "summary",
        "status",
        "version",
        "effective_date",
        "body",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
