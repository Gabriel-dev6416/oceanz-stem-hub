from django.contrib import admin

from .models import TeacherInterest


@admin.register(TeacherInterest)
class TeacherInterestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "whatsapp", "subject_list", "status", "created_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("name", "email", "whatsapp")
    readonly_fields = ("name", "email", "whatsapp", "subject_list", "created_at")
    fields = ("name", "email", "whatsapp", "subject_list", "created_at", "status", "notes")

    @admin.display(description="subjects")
    def subject_list(self, obj):
        return ", ".join(obj.subject_names)

    def has_add_permission(self, request):
        return False
