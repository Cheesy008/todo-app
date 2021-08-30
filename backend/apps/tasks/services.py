from .models import Task
from utils.enums import TaskStatus


def calculate_stats(user_id: int):
    """
    Расчёт статистики по задачам.
    """
    data = dict()

    qs = Task.objects.filter(user_id=user_id)

    data["tasks_done"] = qs.filter(status=TaskStatus.DONE).count()
    data["tasks_total"] = qs.count()
    
    if data['tasks_total'] == 0:
        data["tasks_divided"] = 0
    else:
        number = data["tasks_done"] / data["tasks_total"]
        data["tasks_divided"] = round(number, 2)

    return data
