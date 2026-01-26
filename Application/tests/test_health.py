import pytest

from django.test import Client
from django.urls import reverse
from unittest.mock import Mock, patch

pytestmark = pytest.mark.django_db


@patch("health.views.redis.from_url")
def test_health_check_ok(mock_redis_from_url: Mock, client: Client) -> None:
    mock_redis = Mock()
    mock_redis.ping.return_value = True
    mock_redis_from_url.return_value = mock_redis

    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
        "version": "1.0.0",
    }


@patch("health.views.redis.from_url")
def test_health_check_redis_error(mock_redis_from_url: Mock, client: Client) -> None:
    mock_redis = Mock()
    mock_redis.ping.side_effect = Exception("Redis down")
    mock_redis_from_url.return_value = mock_redis

    response = client.get(reverse("health"))

    assert response.status_code == 503
    assert response.json()["redis"] == "error"
    assert response.json()["status"] == "error"
