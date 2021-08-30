from django.db.models import IntegerChoices


class TaskPriority(IntegerChoices):
    """
    Приоритеты задач.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TaskStatus(IntegerChoices):
    """
    Статусы задач.
    """

    TODO = 1  # Надо сделать
    IN_PROGRESS = 2  # В процессе
    DONE = 3  # Сделана
