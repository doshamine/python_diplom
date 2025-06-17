import pytest
from django.urls import reverse
from backend.models import Order, OrderItem

@pytest.mark.django_db
def test_order_list_empty(auth_client):
    response = auth_client.get(reverse('orders-list'))
    assert response.status_code == 200
    assert response.data == []

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
def test_order_delete(auth_client, order, order_item):
    url = reverse('orders-detail', args=[order.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert Order.objects.count() == 0