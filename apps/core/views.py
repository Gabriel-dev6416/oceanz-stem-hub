import logging

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


def _database_ok():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)
    except Exception:
        logger.exception("Health check: database unavailable")
        return False


def _cache_ok():
    try:
        cache.set("health:ping", "pong", timeout=5)
        return cache.get("health:ping") == "pong"
    except Exception:
        logger.exception("Health check: cache unavailable")
        return False


@never_cache
@require_GET
def health(request):
    """Liveness and dependency check used by Render and uptime monitoring (NFR-15)."""
    checks = {
        "database": "ok" if _database_ok() else "error",
        "cache": "ok" if _cache_ok() else "error",
    }
    healthy = all(value == "ok" for value in checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "error", "checks": checks},
        status=200 if healthy else 503,
    )
