from django.urls import re_path

from . import views
from .models import SLUGS

app_name = "legal"

urlpatterns = [
    re_path(rf"^(?P<slug>{'|'.join(slug for slug, _ in SLUGS)})/$", views.page, name="page"),
]
