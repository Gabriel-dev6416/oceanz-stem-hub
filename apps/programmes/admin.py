from django.contrib import admin

from .models import (
    CurriculumTopic,
    HolidaySession,
    Level,
    LevelSubject,
    PathwayStage,
    TermProject,
    TertiaryPackage,
)


class LevelSubjectInline(admin.TabularInline):
    model = LevelSubject
    extra = 0


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", "classes", "term_fee", "order", "published")
    list_editable = ("term_fee", "order", "published")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [LevelSubjectInline]


@admin.register(PathwayStage)
class PathwayStageAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "published")
    list_editable = ("order", "published")


@admin.register(HolidaySession)
class HolidaySessionAdmin(admin.ModelAdmin):
    list_display = ("name", "fee", "dates", "order", "published")
    list_editable = ("fee", "dates", "order", "published")


@admin.register(TertiaryPackage)
class TertiaryPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "delivery", "order", "published")
    list_editable = ("order", "published")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CurriculumTopic)
class CurriculumTopicAdmin(admin.ModelAdmin):
    list_display = ("class_code", "term", "subject", "week", "title")
    list_filter = ("class_code", "term", "subject")
    search_fields = ("title", "subject", "objectives")


@admin.register(TermProject)
class TermProjectAdmin(admin.ModelAdmin):
    list_display = ("class_code", "term", "title")
    list_filter = ("class_code", "term")
