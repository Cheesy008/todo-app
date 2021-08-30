import json
import pytest
from rest_framework.reverse import reverse


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "username, email, password, password_confirmation, status_code",
    [
        ("user", "test@localhost.com", "password", "password", 200),
        (
            "existing_user",
            "test@localhost.com",
            "password",
            "password",
            400,
        ),  # пользователь с таким ником существует
        ("user", "test@localhost.com", "password", "password123", 400),  # не совпадают пароли
    ],
)
def test_register_view(
    api_client, user_factory, username, email, password, password_confirmation, status_code
):
    endpoint = reverse("auth-register")
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "password_confirmation": password_confirmation,
    }
    user_factory.create(username="existing_user")
    response = api_client.post(endpoint, data=payload, format="json")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("user", "password", 200),
        ("user", "password123", 400),  # некорректный пароль
        ("user123", "password", 400),  # некорректный ник
    ],
)
def test_login_view(api_client, user_factory, username, password, status_code):
    endpoint = reverse("auth-login")
    payload = {
        "username": username,
        "password": password,
    }
    user_factory.create(username="user")
    response = api_client.post(endpoint, data=payload, format="json")
    assert response.status_code == status_code


def test_logout_view(api_client_with_credentials):
    endpoint = reverse("auth-logout")
    response = api_client_with_credentials.post(endpoint)
    assert response.status_code == 204


def test_get_user_view(api_client_with_credentials, user_instance):
    endpoint = reverse("auth-user")
    expected_json = {
        "id": user_instance.id,
        "username": user_instance.username,
        "email": user_instance.email,
    }

    response = api_client_with_credentials.get(endpoint)
    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert parsed_json == expected_json
