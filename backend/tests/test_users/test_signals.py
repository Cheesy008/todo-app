import pytest
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


@pytest.mark.django_db
def test_create_auth_token_signal():
    instance = User(username='user_instance')
    instance.set_password('password')
    instance.save()
    
    _, created = Token.objects.get_or_create(user=instance)
    
    # Проверяем, что сигнал сработал и токен создался.
    assert created == False
    
    