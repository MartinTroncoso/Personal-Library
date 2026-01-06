import json
import pytest
from django.test import Client
from Application.tests.factories.user_factory import UserFactory

pytestmark = pytest.mark.django_db


def test_logout_clears_session() -> None:
    password = "password123"
    user = UserFactory(password=password)

    client = Client(enforce_csrf_checks=True)

    # Login first
    client.get("/auth/login/")
    csrf_token = client.cookies["csrftoken"].value

    client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "username": user.username,
                "password": password,
            }
        ),
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )

    assert "_auth_user_id" in client.session

    # A new CSRF token is generated
    client.get("/auth/login/")
    csrf_token = client.cookies["csrftoken"].value

    # Logout
    response = client.post(
        "/auth/logout/",
        HTTP_X_CSRFTOKEN=csrf_token,
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "_auth_user_id" not in client.session
