import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Order, Contact, OrderStatus


@pytest.mark.django_db
def test_confirm_order_success(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    contact = baker.make(Contact, user=user)

    response = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': contact.id
    })

    order.refresh_from_db()
    assert response.status_code == 200
    assert response.data['message'] == 'Order confirmed successfully.'
    assert order.status == OrderStatus.PAID

@pytest.mark.django_db
def test_confirm_order_not_owned(auth_client):
    other_user_order = baker.make(Order, status=OrderStatus.NEW)
    contact = baker.make(Contact)

    response = auth_client.post(reverse('confirm'), {
        'order_id': other_user_order.id,
        'contact_id': contact.id
    })

    assert response.status_code == 404
    assert response.data['error'] == 'Order not found.'

@pytest.mark.django_db
def test_confirm_order_wrong_status(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.PAID)
    contact = baker.make(Contact, user=user)

    response = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': contact.id
    })

    assert response.status_code == 400
    assert response.data['error'] == 'Only new orders can be confirmed.'

@pytest.mark.django_db
def test_confirm_order_contact_not_found(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)

    response = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': 9999
    })

    assert response.status_code == 404
    assert response.data['error'] == 'Contact not found.'

@pytest.mark.django_db
def test_confirm_order_unauthorized(api_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    contact = baker.make(Contact, user=user)
    response = api_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': contact.id
    })
    assert response.status_code == 401

@pytest.mark.django_db
def test_confirm_order_missing_params(auth_client):
    response = auth_client.post(reverse('confirm'), {})
    assert response.status_code == 400
    assert response.data['error'] == 'order_id and contact_id are required.'

@pytest.mark.django_db
def test_confirm_order_order_not_found(auth_client, user):
    contact = baker.make(Contact, user=user)
    response = auth_client.post(reverse('confirm'), {
        'order_id': 9999,
        'contact_id': contact.id
    })
    assert response.status_code == 404
    assert response.data['error'] == 'Order not found.'

@pytest.mark.django_db
def test_confirm_order_contact_not_owned(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    other_contact = baker.make(Contact)
    response = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': other_contact.id
    })
    assert response.status_code == 404
    assert response.data['error'] == 'Contact not found.'

@pytest.mark.django_db
def test_confirm_order_double_confirm(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    contact = baker.make(Contact, user=user)

    response1 = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': contact.id
    })

    response2 = auth_client.post(reverse('confirm'), {
        'order_id': order.id,
        'contact_id': contact.id
    })

    assert response2.status_code == 400
    assert response2.data['error'] == 'Only new orders can be confirmed.'
