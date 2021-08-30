from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    AuthOutputSerializer,
    UserSerializer,
)
from utils.error_mixin import ApiErrorsMixin


User = get_user_model()


class AuthViewSet(ApiErrorsMixin, viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(method="post", request_body=RegisterSerializer())
    @action(detail=False, methods=["post"])
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        return Response(AuthOutputSerializer({"token": token, "user": user}).data, status.HTTP_200_OK)

    @swagger_auto_schema(method="post", request_body=LoginSerializer())
    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        return Response(
            AuthOutputSerializer({"token": token, "user": user}).data, status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def logout(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(permissions.IsAuthenticated,),
        url_path="user",
        url_name="user",
    )
    def get_user(self, request, *args, **kwargs):
        return Response(
            UserSerializer(request.user).data,
            status.HTTP_200_OK,
        )
