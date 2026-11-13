from itertools import groupby

from django.db.models import Min, Prefetch
from django.shortcuts import get_object_or_404, render

from apps.core.models import FAQ

from .classes import CLASS_NAMES, level_slug
from .forms import ExplorerForm
from .models import (
    CurriculumTopic,
    HolidaySession,
    Level,
    LevelSubject,
    PathwayStage,
    Term,
    TermProject,
    TertiaryPackage,
)


def _levels():
    return Level.objects.filter(published=True).prefetch_related(
        Prefetch("subjects", queryset=LevelSubject.objects.all())
    )


def _sessions():
    return HolidaySession.objects.filter(published=True)


def _packages():
    return TertiaryPackage.objects.filter(published=True)


def _from_fees():
    return {
        "term_from": Level.objects.filter(published=True).aggregate(m=Min("term_fee"))["m"],
        "holiday_from": _sessions().aggregate(m=Min("fee"))["m"],
    }


def overview(request):
    """Programmes overview (FR-WEB-03)."""
    levels = list(_levels())
    return render(
        request,
        "programmes/overview.html",
        {
            "page_title": "Programmes",
            "primary_levels": [lv for lv in levels if lv.group == Level.Group.PRIMARY],
            "secondary_levels": [lv for lv in levels if lv.group == Level.Group.SECONDARY],
            "levels": levels,
            "sessions": _sessions(),
            "packages": _packages(),
            "faqs": FAQ.objects.filter(published=True),
            **_from_fees(),
        },
    )


def level(request, slug):
    level = get_object_or_404(_levels().select_related("stage"), slug=slug)
    return render(
        request,
        "programmes/level.html",
        {"page_title": level.name, "level": level, "sessions": _sessions()},
    )


def holiday(request):
    return render(
        request,
        "programmes/holiday.html",
        {"page_title": "Holiday Tuition", "sessions": _sessions(), "levels": _levels()},
    )


def tertiary(request):
    return render(
        request,
        "programmes/tertiary.html",
        {"page_title": "Tertiary packages", "packages": _packages()},
    )


def package(request, slug):
    package = get_object_or_404(_packages(), slug=slug)
    return render(
        request,
        "programmes/package.html",
        {"page_title": package.name, "package": package, "packages": _packages()},
    )


def subjects(request):
    """Subjects and the STEM pathway (FR-WEB-04)."""
    return render(
        request,
        "programmes/subjects.html",
        {
            "page_title": "Subjects",
            "stages": PathwayStage.objects.filter(published=True),
            "levels": _levels(),
        },
    )


def pricing(request):
    """Pricing in Naira, with quote cards for fees that are never published (FR-WEB-05)."""
    return render(
        request,
        "programmes/pricing.html",
        {"page_title": "Pricing", "levels": _levels(), "sessions": _sessions()},
    )


def explorer(request):
    """'See what your child will learn' (FR-ENG-01, decision D-01)."""
    form = ExplorerForm(request.GET or None)
    context = {"page_title": "See what your child will learn", "form": form}
    if form.is_valid():
        class_code = form.cleaned_data["class_code"]
        term = form.cleaned_data["term"]
        topics = CurriculumTopic.objects.filter(class_code=class_code, term=term).order_by(
            "subject", "week"
        )
        by_subject = groupby(topics, key=lambda topic: topic.subject)
        level = _levels().select_related("stage").filter(slug=level_slug(class_code))
        context.update(
            {
                "class_name": CLASS_NAMES[class_code],
                "term_name": Term(term).label,
                "topics_by_subject": [(subject, list(items)) for subject, items in by_subject],
                "project": TermProject.objects.filter(class_code=class_code, term=term).first(),
                "level": level.first(),
            }
        )
    return render(request, "programmes/explorer.html", context)
