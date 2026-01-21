import pytest

from django.conf import settings
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from Application.tests.factories.user_factory import UserFactory
from authentication.services import AuthService

pytestmark = pytest.mark.django_db


def test_user_creation() -> None:
    user = UserFactory()

    assert user.id is not None
    assert user.check_password("password123")


@pytest.mark.django_db
def test_django_settings_loaded() -> None:
    assert settings.DEBUG is not None


@pytest.mark.django_db
def test_login_service_success() -> None:
    user = UserFactory(password="123456")

    factory = RequestFactory()
    request = factory.post("/auth/login/")

    # Add session to request
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()

    success = AuthService.login_user(request, user.username, "123456")

    assert success is True
    assert "_auth_user_id" in request.session
