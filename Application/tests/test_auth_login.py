import json
import pytest
from django.test import Client
from Application.tests.factories.user_factory import UserFactory

pytestmark = pytest.mark.django_db


def test_login_success_creates_session() -> None:
    password = "password123"
    user = UserFactory(password=password)

    client = Client(enforce_csrf_checks=True)

    # Get CSRF
    client.get("/auth/login/")
    csrf_token = client.cookies["csrftoken"].value

    response = client.post(
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

    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify session
    assert "_auth_user_id" in client.session
