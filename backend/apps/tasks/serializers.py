from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для получения и создания задач.
    """
    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "description",
            "end_date",
            "priority",
            "status",
        )
        read_only_fields = ("user",)
