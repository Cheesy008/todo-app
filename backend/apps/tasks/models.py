from django.db import models

from utils.enums import TaskPriority, TaskStatus


class Task(models.Model):
    """
    Модель задачи.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь",
    )
    description = models.CharField("Описание", max_length=225)
    priority = models.PositiveSmallIntegerField(
        "Приоритет", choices=TaskPriority.choices, null=True
    )
    status = models.PositiveSmallIntegerField(
        "Статус", choices=TaskPriority.choices, default=TaskStatus.TODO
    )
    end_date = models.DateField("Дедлайн", null=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self) -> str:
        return self.description
