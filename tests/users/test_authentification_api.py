import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def registered_user(user_data):
    user = User.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"]
    )
    return user

@pytest.mark.django_db
def test_user_registration(api_client, user_data):
    url = reverse('register')
    response = api_client.post(url, user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data
    assert User.objects.filter(email=user_data['email']).exists()

@pytest.mark.django_db
def test_user_login(api_client, registered_user, user_data):
    url = reverse('login')
    credentials = {
        'username': user_data['username'],
        'password': user_data['password']
    }
    response = api_client.post(url, credentials)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data