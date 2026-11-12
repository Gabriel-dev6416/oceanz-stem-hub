from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("enquire/", views.enquire, name="enquire"),
    path("enquire/received/", views.received, name="received"),
    path("contact/", views.contact, name="contact"),
]
