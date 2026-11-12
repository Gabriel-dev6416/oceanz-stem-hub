import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_reports_database_and_cache_ok(client):
    response = client.get(reverse("core:health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok", "cache": "ok"}}
    assert "no-cache" in response["Cache-Control"]


def test_health_rejects_post(client):
    response = client.post(reverse("core:health"))

    assert response.status_code == 405
