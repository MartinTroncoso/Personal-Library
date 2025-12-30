import pytest
from django.conf import settings


@pytest.mark.django_db
def test_django_settings_loaded() -> None:
    assert settings.DEBUG is not None
