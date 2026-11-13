from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("results/", views.results, name="results"),
    path("diaspora/", views.diaspora, name="diaspora"),
    path("health/", views.health, name="health"),
]
