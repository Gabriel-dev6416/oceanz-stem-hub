from django.urls import path

from . import views

app_name = "programmes"

urlpatterns = [
    path("programmes/", views.overview, name="overview"),
    path("programmes/holiday-tuition/", views.holiday, name="holiday"),
    path("programmes/tertiary/", views.tertiary, name="tertiary"),
    path("programmes/tertiary/<slug:slug>/", views.package, name="package"),
    path("programmes/explorer/", views.explorer, name="explorer"),
    path("programmes/<slug:slug>/", views.level, name="level"),
    path("subjects/", views.subjects, name="subjects"),
    path("pricing/", views.pricing, name="pricing"),
]
