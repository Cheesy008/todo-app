from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .services import register_user, login_user


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации пользователя.
    """

    password = serializers.CharField(
        min_length=6,
        max_length=68,
        style={"input_type": "password"},
        required=True,
        write_only=True,
    )
    password_confirmation = serializers.CharField(
        min_length=6,
        max_length=68,
        style={"input_type": "password"},
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirmation")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise ValidationError("Пароли не совпадают")

        attrs.pop("password_confirmation")

        return attrs

    def create(self, validated_data):
        token, user = register_user(**validated_data)
        return token, user


class LoginSerializer(serializers.Serializer):
    """
    Сериалайзер для авторизации пользователя.
    """

    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

    def create(self, validated_data):
        token, user = login_user(**validated_data)
        return token, user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода данных о пользователе.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("__all__",)


class AuthOutputSerializer(serializers.Serializer):
    """
    Сериалайзер для вывода токена и пользователя.
    """

    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
