import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_product_list(api_client, product):
    url = reverse('products-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1