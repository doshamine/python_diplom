import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Contact

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
def test_contact_delete(auth_client, user):
    contact = baker.make('backend.Contact', user=user, type='phone', value='+123456789')
    url = reverse('contacts-detail', args=[contact.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Contact.objects.count() == 0