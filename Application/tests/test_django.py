import pytest
from django.conf import settings
from Application.tests.factories.user_factory import UserFactory

pytestmark = pytest.mark.django_db


def test_user_creation() -> None:
    user = UserFactory()

    assert user.id is not None
    assert user.check_password("password123")


@pytest.mark.django_db
def test_django_settings_loaded() -> None:
    assert settings.DEBUG is not None
