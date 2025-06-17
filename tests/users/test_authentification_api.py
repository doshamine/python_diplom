import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'new@example.com',
        'password': 'secret123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert 'token' in response.data


@pytest.mark.django_db
def test_login_user(api_client):
    user = User.objects.create_user(username='loginuser', password='pass1234')
    Token.objects.create(user=user)

    url = reverse('login')
    response = api_client.post(url, {
        'username': 'loginuser',
        'password': 'pass1234'
    })

    assert response.status_code == 200
    assert 'token' in response.data