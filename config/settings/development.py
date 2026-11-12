from .base import *  # noqa: F403
from .base import STORAGES, env

DEBUG = env.bool("DJANGO_DEBUG", default=True)

# Hashed, compressed static files need collectstatic, which only runs in the Docker build.
STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
