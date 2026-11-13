from django.shortcuts import get_object_or_404, render

from .models import LegalPage


def page(request, slug):
    legal = get_object_or_404(LegalPage, slug=slug)
    return render(request, "legal/page.html", {"page_title": legal.title, "legal": legal})
