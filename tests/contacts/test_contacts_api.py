import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Contact


@pytest.mark.django_db
def test_contact_list_unauthorized(api_client):
    url = reverse('contacts-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_contact_list_empty(auth_client):
    url = reverse('contacts-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_contact_create(auth_client):
    url = reverse('contacts-list')
    data = {
        'type': 'email',
        'value': 'user@example.com'
    }
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert Contact.objects.count() == 1
    contact = Contact.objects.first()
    assert contact.type == 'email'
    assert contact.value == 'user@example.com'


@pytest.mark.django_db
def test_contact_create_unauthorized(api_client):
    url = reverse('contacts-list')
    data = {'type': 'email', 'value': 'user@example.com'}
    response = api_client.post(url, data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_contact_list_only_own(auth_client, user):
    contact1 = baker.make('backend.Contact', user=user, type='email', value='me@example.com')

    baker.make('backend.Contact', type='phone', value='+111111111')
    url = reverse('contacts-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == contact1.id


@pytest.mark.django_db
def test_contact_update(auth_client, user):
    contact = baker.make('backend.Contact', user=user, type='phone', value='+123456789')
    url = reverse('contacts-detail', args=[contact.id])
    data = {'type': 'phone', 'value': '+987654321'}
    response = auth_client.put(url, data)
    assert response.status_code == 200
    contact.refresh_from_db()
    assert contact.value == '+987654321'


@pytest.mark.django_db
def test_contact_delete(auth_client, user):
    contact = baker.make('backend.Contact', user=user, type='phone', value='+123456789')
    url = reverse('contacts-detail', args=[contact.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Contact.objects.count() == 0


@pytest.mark.django_db
def test_contact_delete_not_owned(auth_client):
    contact = baker.make('backend.Contact', type='phone', value='+111111111')
    url = reverse('contacts-detail', args=[contact.id])
    response = auth_client.delete(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_contact_create_invalid(auth_client):
    url = reverse('contacts-list')
    data = {'type': 'email'}
    response = auth_client.post(url, data)
    assert response.status_code == 400
    assert 'value' in response.data
