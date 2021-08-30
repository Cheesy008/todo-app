import pytest

from apps.tasks.services import calculate_stats
from utils.enums import TaskStatus


@pytest.mark.django_db
def test_calculate_stats(create_task_batch, user_instance):
    create_task_batch(3, status=TaskStatus.DONE)
    create_task_batch(2, status=TaskStatus.IN_PROGRESS)
    
    expected_data = {
        'tasks_done': 3,
        'tasks_total': 5,
        'tasks_divided': 0.6
    }
    
    data = calculate_stats(user_instance.id)
    assert data == expected_data

