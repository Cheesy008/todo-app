from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


def register_user(*, username: str, email: str, password: str) -> tuple[str, User]:
    """
    Создание пользователя и генерация токена.
    """
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.get(user=user).key
    return token, user


def login_user(*, username: str, password: str) -> tuple[str, User]:
    """
    Авторизация пользователя.

    Если предоставленные данные валидны, то генерирурем токен
    и возвращаем его.
    """
    user = authenticate(username=username, password=password)
    if not user:
        raise ValidationError("Неверные данные пользователя")

    token, _ = Token.objects.get_or_create(user=user)

    return token.key, user
