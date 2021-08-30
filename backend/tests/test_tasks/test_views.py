from datetime import datetime
import pytest
import json
from rest_framework.reverse import reverse

from utils.enums import TaskStatus, TaskPriority


pytestmark = [pytest.mark.django_db]


DATETIME_FORMAT = "%Y-%m-%d"


def test_task_view_unathorized(api_client):
    """Тест, что неавторизованный пользователь не может совершить запрос."""

    endpoint = reverse("task-list")
    response = api_client.get(endpoint)
    assert response.status_code == 401


def test_list_task_view(api_client_with_credentials, create_task_batch):
    """Тест получения списка задач."""

    create_task_batch(5)

    endpoint = reverse("task-list")
    response = api_client_with_credentials.get(endpoint)
    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert len(parsed_json) == 5


def test_get_task_view(api_client_with_credentials, user_instance, create_task):
    """Тест получения конкретного экземпляра задачи."""

    task_instance = create_task()
    expected_json = {
        "id": task_instance.id,
        "user": user_instance.id,
        "description": task_instance.description,
        "end_date": task_instance.end_date.strftime(DATETIME_FORMAT),
        "priority": task_instance.priority,
        "status": task_instance.status,
    }

    endpoint = reverse("task-detail", kwargs={"pk": task_instance.id})
    response = api_client_with_credentials.get(endpoint)
    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert parsed_json == expected_json


@pytest.mark.django_db(reset_sequences=True)
def test_create_task_view(api_client_with_credentials, user_instance, task_factory):
    """Тест создания задачи."""

    task = task_factory.build(user=user_instance, status=TaskStatus.TODO)
    expected_json = {
        "id": 1,
        "user": user_instance.id,
        "description": task.description,
        "end_date": task.end_date,
        "priority": task.priority,
        "status": task.status,
    }

    endpoint = reverse("task-list")
    response = api_client_with_credentials.post(
        endpoint, data=expected_json, format="json"
    )
    parsed_json = json.loads(response.content)

    #  Преобразуем объект datetime в строку, чтобы сравнение было корректным.
    expected_json["end_date"] = expected_json["end_date"].strftime(DATETIME_FORMAT)

    assert response.status_code == 201
    assert parsed_json == expected_json


@pytest.mark.parametrize(
    "field",
    [
        "description",
        "end_date",
        "priority",
        "status",
    ],
)
def test_patch_task_view(api_client_with_credentials, create_task, field):
    """
    Тестирование обновление задачи.

    Через parametrize передаём по одному полю и проверяем,
    что задача корректно обновилась.
    """

    task_instance = create_task()
    endpoint = reverse("task-detail", kwargs={"pk": task_instance.id})
    payload = {
        "description": "some task",
        "end_date": datetime.now().strftime(DATETIME_FORMAT),
        "priority": TaskPriority.HIGH,
        "status": TaskStatus.IN_PROGRESS,
    }
    valid_field = payload[field]

    response = api_client_with_credentials.patch(
        endpoint, data={field: valid_field}, format="json"
    )
    assert response.status_code == 200
    assert response.data[field] == payload[field]


def test_delete_task_view(api_client_with_credentials, create_task):
    """Тест удаления задачи."""

    task_instance = create_task()
    endpoint = reverse("task-detail", kwargs={"pk": task_instance.id})
    response = api_client_with_credentials.delete(endpoint)

    assert response.status_code == 204


@pytest.mark.parametrize(
    "status, count",
    [
        (TaskStatus.TODO, 5),
        (TaskStatus.IN_PROGRESS, 7),
        (TaskStatus.DONE, 3),
    ],
)
def test_search_status_task(api_client_with_credentials, create_task_batch, status, count):
    """Тест на поиск задач по статусу."""

    create_task_batch(5, status=TaskStatus.TODO)
    create_task_batch(7, status=TaskStatus.IN_PROGRESS)
    create_task_batch(3, status=TaskStatus.DONE)

    endpoint = f"{reverse('task-list')}?status={status}"
    response = api_client_with_credentials.get(endpoint)

    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert len(parsed_json) == count


@pytest.mark.parametrize(
    "priority, count",
    [
        (TaskPriority.LOW, 5),
        (TaskPriority.MEDIUM, 7),
        (TaskPriority.HIGH, 3),
    ],
)
def test_search_priority_task(api_client_with_credentials, create_task_batch, priority, count):
    """Тест на поиск задач по приоритету."""

    create_task_batch(5, priority=TaskPriority.LOW)
    create_task_batch(7, priority=TaskPriority.MEDIUM)
    create_task_batch(3, priority=TaskPriority.HIGH)

    endpoint = f"{reverse('task-list')}?priority={priority}"
    response = api_client_with_credentials.get(endpoint)

    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert len(parsed_json) == count



@pytest.mark.parametrize(
    "date, count",
    [
        ("2021-07-04", 5),
        ("2021-07-05", 7),
        ("2021-07-06", 3),
    ],
)
def test_search_end_date_task(api_client_with_credentials, create_task_batch, date, count):
    """Тест на поиск задач по дате."""

    create_task_batch(5, end_date="2021-07-04")
    create_task_batch(7, end_date="2021-07-05")
    create_task_batch(3, end_date="2021-07-06")

    endpoint = f"{reverse('task-list')}?end_date={date}"
    response = api_client_with_credentials.get(endpoint)

    parsed_json = json.loads(response.content)

    assert response.status_code == 200
    assert len(parsed_json) == count
