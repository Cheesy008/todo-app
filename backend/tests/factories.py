from datetime import date

import factory
from factory import fuzzy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save

from apps.tasks.models import Task
from utils.enums import TaskStatus, TaskPriority


User = get_user_model()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    password = factory.LazyFunction(lambda: make_password("password"))  # пароль создаётся по умолчанию для всех пользователей


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    description = factory.Sequence(lambda n: "Task {}".format(n))
    priority = fuzzy.FuzzyChoice(TaskPriority.choices, getter=lambda c: c[0])
    status = fuzzy.FuzzyChoice(TaskStatus.choices, getter=lambda c: c[0])
    end_date = fuzzy.FuzzyDate(
        date(2021, 1, 1), date(2021, 1, 10)
    )
