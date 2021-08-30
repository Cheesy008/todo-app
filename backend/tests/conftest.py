import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .factories import UserFactory, TaskFactory


register(UserFactory)
register(TaskFactory)


@pytest.fixture
def user_instance(db, user_factory):
    """
    Тестовый пользователь, от которого будут идти
    все запросы.
    """
    return user_factory.create()


@pytest.fixture
def api_client():
    """
    Фикстура api_client, для тестирования неавторизованного пользователя.
    """
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, user_instance):
    """
    Авторизованный api_client.
    """
    client = APIClient()
    token = Token.objects.create(user=user_instance)
    client.force_authenticate(user=user_instance, token=token)
    return client


@pytest.fixture
def create_task(db, task_factory, user_instance):
    def task(**kwargs):
        return task_factory.create(user=user_instance, **kwargs)

    return task


@pytest.fixture
def create_task_batch(db, task_factory, user_instance):
    def task_batch(n, **kwargs):
        return task_factory.create_batch(n, user=user_instance, **kwargs)

    return task_batch
