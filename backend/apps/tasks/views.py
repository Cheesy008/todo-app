from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TaskSerializer
from .models import Task
from .tasks import send_email_stats
from .services import calculate_stats


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ("status", "priority", "end_date")
    search_fields = ("status", "priority", "end_date")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="send-stats")
    def send_stats(self, request, *args, **kwargs):
        user = request.user
        data = calculate_stats(user.id)
        send_email_stats.delay(data, user.email)

        return Response(
            {"message": "Статистика отправлена на почту"},
            status=status.HTTP_200_OK,
        )
