import pytest
from django.urls import reverse
from model_bakery import baker
from backend.models import Order, OrderStatus, OrderItem


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