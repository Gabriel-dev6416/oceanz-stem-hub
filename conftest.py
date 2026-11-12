import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def _clear_cache():
    """Cached singletons must not leak between tests whose database changes roll back."""
    cache.clear()
    yield
    cache.clear()
