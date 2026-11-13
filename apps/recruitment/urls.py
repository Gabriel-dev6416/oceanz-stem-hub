from django.urls import path

from . import views

app_name = "recruitment"

urlpatterns = [
    path("teach-with-us/", views.teach_with_us, name="teach_with_us"),
    path("teach-with-us/thanks/", views.thanks, name="thanks"),
]
