from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("", include("apps.messaging.urls")),
    path("", include("apps.core.urls")),
]

handler500 = "apps.core.views.server_error"
