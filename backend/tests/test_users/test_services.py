import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from apps.users.services import register_user, login_user


User = get_user_model()


pytestmark = [pytest.mark.django_db]


def test_register_user_service():
    payload = {"username": "user1", "email": "test@user.com", "password": "password"}

    token, user = register_user(**payload)

    assert User.objects.count() == 1
    assert Token.objects.get(user=user).key == token


def test_login_user_service(user_factory):
    user = user_factory.create(username="user")
    payload = {"username": user.username, "password": "password"}

    token, user = login_user(**payload)

    assert User.objects.count() == 1
    assert Token.objects.get(user=user).key == token


def test_login_user_service_auth_failed(user_factory):
    """
    Провальный тест для сервиса логина (передаётся некорректный пароль).
    """
    user = user_factory.create(username="user")
    payload = {"username": user.username, "password": "password1"}

    with pytest.raises(ValidationError):
        login_user(**payload)
