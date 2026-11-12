from django.contrib import admin, messages

from .emails import send_reply
from .models import Enquiry, EnquiryNote, EnquiryReply


class NoteInline(admin.StackedInline):
    model = EnquiryNote
    extra = 0
    fields = ("text", "author", "created_at")
    readonly_fields = ("author", "created_at")
    verbose_name = "internal note (never sent)"

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReplyInline(admin.StackedInline):
    model = EnquiryReply
    extra = 0
    fields = ("body", "author", "sent_at")
    readonly_fields = ("author", "sent_at")
    verbose_name = "email reply (sent to the enquirer when you save)"
    verbose_name_plural = "email replies"

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def _status_action(status):
    def action(modeladmin, request, queryset):
        updated = queryset.update(status=status)
        modeladmin.message_user(request, f"{updated} enquiries marked {status.label.lower()}.")

    action.__name__ = f"mark_{status.value.replace('-', '_')}"
    action.short_description = f"Mark selected as {status.label.lower()}"
    return action


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    """Enquiry management (FR-COM-02)."""

    list_display = (
        "reference",
        "created_at",
        "enquiry_type",
        "name",
        "phone",
        "child_class",
        "status",
        "assigned_to",
    )
    list_filter = ("status", "enquiry_type", "assigned_to", "delivery_format", "created_at")
    search_fields = ("reference", "name", "email", "phone", "whatsapp")
    date_hierarchy = "created_at"
    list_select_related = ("assigned_to",)
    fieldsets = (
        ("Handling", {"fields": ("status", "assigned_to")}),
        (
            "Enquiry",
            {
                "fields": (
                    "reference",
                    "created_at",
                    "enquiry_type",
                    "name",
                    "email",
                    "phone",
                    "whatsapp",
                    "child_class",
                    "tutoring_option",
                    "delivery_format",
                    "message",
                    "source_page",
                )
            },
        ),
    )
    readonly_fields = (
        "reference",
        "created_at",
        "enquiry_type",
        "name",
        "email",
        "phone",
        "whatsapp",
        "child_class",
        "tutoring_option",
        "delivery_format",
        "message",
        "source_page",
    )
    inlines = [NoteInline, ReplyInline]
    actions = [_status_action(status) for status in Enquiry.Status]

    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            obj.author = request.user
            obj.save()
            if isinstance(obj, EnquiryReply):
                if send_reply(obj):
                    messages.success(request, f"Reply emailed to {obj.enquiry.email}.")
                else:
                    messages.error(
                        request,
                        "The reply was saved but the email could not be sent. Check the email "
                        "settings and send it again.",
                    )
        formset.save_m2m()
