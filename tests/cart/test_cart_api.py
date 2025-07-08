import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Order, OrderStatus, OrderItem, ProductInfo


@pytest.mark.django_db
def test_cart_empty(auth_client):
    url = reverse('cart-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_cart_with_items(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)

    url = reverse('cart-list')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['id'] == order.id
    assert response.data[0]['status'] == OrderStatus.NEW
    assert len(response.data[0]['order_items']) == 1
    assert response.data[0]['order_items'][0]['quantity'] == 2

@pytest.mark.django_db
def test_cart_order_items_fields(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    order_item = baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)
    url = reverse('cart-list')
    response = auth_client.get(url)
    item = response.data[0]['order_items'][0]
    assert item['product'] == product.id
    assert item['shop'] == shop.id
    assert item['quantity'] == 2

@pytest.mark.parametrize("status", [OrderStatus.SHIPPED, OrderStatus.CANCELED])
@pytest.mark.django_db
def test_cart_with_non_new_statuses(auth_client, user, status):
    baker.make(Order, user=user, status=status)
    url = reverse('cart-list')
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cart_with_multiple_items(auth_client, user, product, shop):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    product2 = baker.make('backend.Product')
    baker.make(OrderItem, order=order, product=product, shop=shop, quantity=2)
    baker.make(OrderItem, order=order, product=product2, shop=shop, quantity=3)

    url = reverse('cart-list')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['id'] == order.id
    assert len(response.data[0]['order_items']) == 2
    quantities = [item['quantity'] for item in response.data[0]['order_items']]
    assert 2 in quantities and 3 in quantities

@pytest.mark.django_db
def test_cart_does_not_show_other_users_order(auth_client, user):
    other_user = baker.make('auth.User')
    order = baker.make(Order, user=other_user, status=OrderStatus.NEW)
    url = reverse('cart-list')
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_cart_order_without_items(auth_client, user):
    order = baker.make(Order, user=user, status=OrderStatus.NEW)
    url = reverse('cart-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['id'] == order.id
    assert response.data[0]['order_items'] == []

@pytest.mark.django_db
def test_cart_unauthorized(api_client):
    url = reverse('cart-list')
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_cart_add_item_with_insufficient_stock(auth_client, user, product, shop):
    product_info = baker.make(ProductInfo, product=product, shop=shop, quantity=1)
    order = baker.make(Order, user=user, status=OrderStatus.NEW)

    data = {
        "order_items": [
            {"product": product.id, "shop": shop.id, "quantity": 2}
        ]
    }
    url = reverse('orders-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'Only' in str(response.data)

@pytest.mark.django_db
def test_cart_duplicate_order_items_validation(auth_client, user, product, shop):
    product_info = baker.make(ProductInfo, product=product, shop=shop, quantity=3)

    data = {
        "order_items": [
            {"product": product.id, "shop": shop.id, "quantity": 1},
            {"product": product.id, "shop": shop.id, "quantity": 2}
        ]
    }
    url = reverse('orders-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'You cannot add multiple items with the same product and store in one order.' in str(response.data)

@pytest.mark.django_db
def test_cart_serializer_error(auth_client, user):

    data = {"order_items": [{"product": None, "shop": None, "quantity": None}]}
    url = reverse('orders-list')
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'errors' in response.data or isinstance(response.data, dict)

