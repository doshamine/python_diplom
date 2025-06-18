import pytest
from django.urls import reverse
from model_bakery import baker

from backend.models import Order, OrderItem, OrderStatus


@pytest.mark.django_db
def test_order_list_empty(auth_client):
    response = auth_client.get(reverse('orders-list'))
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_order_list_unauthorized(api_client):
    response = api_client.get(reverse('orders-list'))
    assert response.status_code == 401


@pytest.mark.django_db
def test_order_create(auth_client, product, shop):
    url = reverse('orders-list')
    payload = {
        "status": "new",
        "order_items": [
            {
                "product": product.id,
                "shop": shop.id,
                "quantity": 2
            }
        ]
    }
    response = auth_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1


@pytest.mark.django_db
def test_order_create_invalid(auth_client, product, shop):
    url = reverse('orders-list')
    payload = {
        "status": "new",
        "order_items": [
            {
                "shop": shop.id,
                "quantity": 2
            }
        ]
    }
    response = auth_client.post(url, payload, format='json')
    assert response.status_code == 400
    assert 'product' in response.data.get('order_items', [{}])[0]



@pytest.mark.django_db
def test_order_retrieve(auth_client, user, product, shop):
    order = Order.objects.create(user=user, status=OrderStatus.PAID)
    OrderItem.objects.create(order=order, product=product, shop=shop, quantity=1)
    url = reverse('orders-detail', args=[order.id])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == order.id


@pytest.mark.django_db
def test_order_retrieve_not_owned(auth_client, user, product, shop):
    other_user = baker.make('auth.User')
    order = Order.objects.create(user=other_user, status=OrderStatus.PAID)
    url = reverse('orders-detail', args=[order.id])
    response = auth_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_order_update(auth_client, user, product, shop):
    order = Order.objects.create(user=user, status=OrderStatus.PAID)
    OrderItem.objects.create(order=order, product=product, shop=shop, quantity=1)
    url = reverse('orders-detail', args=[order.id])
    data = {'status': 'canceled'}
    response = auth_client.patch(url, data, format='json')
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == OrderStatus.CANCELED


@pytest.mark.django_db
def test_order_create_unauthorized(api_client, product, shop):
    url = reverse('orders-list')
    payload = {
        "status": "new",
        "order_items": [
            {
                "product": product.id,
                "shop": shop.id,
                "quantity": 2
            }
        ]
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_order_list_only_own(auth_client, user, product, shop):
    order1 = Order.objects.create(user=user, status=OrderStatus.PAID)
    OrderItem.objects.create(order=order1, product=product, shop=shop, quantity=1)

    other_user = baker.make('auth.User')
    Order.objects.create(user=other_user, status=OrderStatus.PAID)
    response = auth_client.get(reverse('orders-list'))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == order1.id


@pytest.mark.django_db
def test_order_delete_not_owned(auth_client, user, product, shop):
    other_user = baker.make('auth.User')
    order = Order.objects.create(user=other_user, status=OrderStatus.PAID)
    url = reverse('orders-detail', args=[order.id])
    response = auth_client.delete(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_order_delete(auth_client, user, product, shop):
    order = Order.objects.create(user=user, status=OrderStatus.PAID)
    OrderItem.objects.create(order=order, product=product, shop=shop, quantity=1)
    url = reverse('orders-detail', args=[order.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Order.objects.count() == 0
