import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Order, OrderStatus, OrderItem, ProductInfo


@pytest.mark.django_db
def test_cart_empty(auth_client):
    url = reverse('cart')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['message'] == 'Cart is empty'


@pytest.mark.django_db
def test_cart_with_items(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)

    url = reverse('cart')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == order.id
    assert response.data['status'] == OrderStatus.NEW
    assert len(response.data['order_items']) == 1
    assert response.data['order_items'][0]['quantity'] == 2


@pytest.mark.django_db
def test_cart_order_items_fields(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    order_item = baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)
    url = reverse('cart')
    response = auth_client.get(url)
    item = response.data['order_items'][0]
    assert item['product'] == product.id
    assert item['shop'] == shop.id
    assert item['quantity'] == 2


@pytest.mark.parametrize("status", [OrderStatus.SHIPPED, OrderStatus.CANCELED])
@pytest.mark.django_db
def test_cart_with_non_new_statuses(auth_client, user, status):
    baker.make(Order, user=user, status=status)
    url = reverse('cart')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['message'] == 'Cart is empty'


@pytest.mark.django_db
def test_cart_with_multiple_items(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    product2 = baker.make('backend.Product')
    baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)
    baker.make(OrderItem, order=order, product=product2, shop=shop, quantity=3)

    url = reverse('cart')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == order.id
    assert len(response.data['order_items']) == 2
    quantities = [item['quantity'] for item in response.data['order_items']]
    assert 2 in quantities and 3 in quantities

@pytest.mark.django_db
def test_cart_does_not_show_other_users_order(auth_client, user):
    other_user = baker.make('auth.User')
    order = baker.make(Order, user=other_user, status=OrderStatus.NEW)
    url = reverse('cart')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['message'] == 'Cart is empty'

@pytest.mark.django_db
def test_cart_order_without_items(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    url = reverse('cart')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == order.id
    assert response.data['order_items'] == []

@pytest.mark.django_db
def test_cart_server_error(monkeypatch, auth_client):
    def raise_exception(*args, **kwargs):
        raise Exception("Test error")
    monkeypatch.setattr('backend.views.Order.objects.filter', raise_exception)
    url = reverse('cart')
    response = auth_client.get(url)
    assert response.status_code == 500
    assert 'error' in response.data

@pytest.mark.django_db
def test_cart_unauthorized(api_client):
    url = reverse('cart')
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_cart_add_item_with_insufficient_stock(auth_client, user, product, shop):
    ProductInfo.objects.filter(product=product, shop=shop).update(quantity=1)
    order = baker.make(Order, user=user, status=OrderStatus.NEW)

    data = {
        "order_items": [
            {"product": product.id, "shop": shop.id, "quantity": 2}
        ]
    }
    url = reverse('order-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'Недостаточно товара' in str(response.data)

@pytest.mark.django_db
def test_cart_duplicate_order_items_validation(auth_client, user, product, shop):
    data = {
        "order_items": [
            {"product": product.id, "shop": shop.id, "quantity": 1},
            {"product": product.id, "shop": shop.id, "quantity": 2}
        ]
    }
    url = reverse('order-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'Нельзя добавлять несколько позиций с одинаковыми товаром и магазином' in str(response.data)

@pytest.mark.django_db
def test_cart_serializer_error(auth_client, user):

    data = {"order_items": [{"product": None, "shop": None, "quantity": None}]}
    url = reverse('order-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'errors' in response.data or isinstance(response.data, dict)

