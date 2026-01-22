import pytest
from Application.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_password_is_hashed() -> None:
    user = UserFactory(password="123456")

    assert user.password != "123456a"
    assert user.password.startswith("pbkdf2")


@pytest.mark.django_db
def test_check_password() -> None:
    user = UserFactory(password="123456")

    assert user.check_password("123456") is True
    assert user.check_password("wrong") is False
