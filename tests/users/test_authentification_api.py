import pytest
from django.core import mail
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
def test_register_user_duplicate_username(api_client):
    User.objects.create_user(username='newuser', password='pass')
    url = reverse('register')
    data = {
        'username': 'newuser',
        'first_name': 'Another',
        'last_name': 'User',
        'email': 'another@example.com',
        'password': 'secret123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert 'username' in response.data


@pytest.mark.django_db
def test_register_user_invalid_data(api_client):
    url = reverse('register')
    data = {
        'username': '',
        'password': 'short'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert 'username' in response.data


@pytest.mark.django_db
def test_register_user_no_password(api_client):
    url = reverse('register')
    data = {
        'username': 'nopass',
        'first_name': 'No',
        'last_name': 'Pass',
        'email': 'nopass@example.com'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert 'password' in response.data



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


@pytest.mark.django_db
def test_login_user_wrong_password(api_client):
    User.objects.create_user(username='wrongpass', password='rightpass')
    url = reverse('login')
    response = api_client.post(url, {
        'username': 'wrongpass',
        'password': 'wrongpass'
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_not_found(api_client):
    url = reverse('login')
    response = api_client.post(url, {
        'username': 'nouser',
        'password': 'nopass'
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_sends_email(api_client):
    url = reverse('register')
    data = {
        'username': 'mailuser',
        'first_name': 'Mail',
        'last_name': 'User',
        'email': 'mailuser@example.com',
        'password': 'secret123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == ['mailuser@example.com']
    assert 'регистрация' in email.subject
    assert 'Спасибо' in email.body


@pytest.mark.django_db
def test_register_user_no_email_sent_on_invalid_data(api_client):
    url = reverse('register')
    data = {
        'username': '',
        'email': 'fail@example.com',
        'password': 'short'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert len(mail.outbox) == 0