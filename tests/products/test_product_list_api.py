import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import ProductInfo

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product_setup():
    product_info = baker.make(ProductInfo, _quantity=1, make_m2m=True)[0]
    product = product_info.product

    return product


@pytest.mark.django_db
def test_product_list(api_client, product_setup):
    url = '/api/v1/products/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_product_search(api_client):
    product = baker.make('backend.Product', name='TestPhone', model='X100')
    baker.make('backend.ProductInfo', product=product, make_m2m=True)

    url = '/api/v1/products/'
    response = api_client.get(url, {'search': 'X100'})
    assert response.status_code == status.HTTP_200_OK
    assert any(prod['model'] == 'X100' for prod in response.data)


@pytest.mark.django_db
def test_product_filter_by_price(api_client):
    product_info = baker.make('backend.ProductInfo', price=500.00, make_m2m=True)

    url = '/api/v1/products/'
    response = api_client.get(url, {'min_price': 400, 'max_price': 600})
    assert response.status_code == status.HTTP_200_OK
    assert any(prod['id'] == product_info.product.id for prod in response.data)


@pytest.mark.django_db
def test_product_filter_by_shop(api_client):
    product_info = baker.make('backend.ProductInfo', make_m2m=True)
    shop_id = product_info.shop.id

    url = '/api/v1/products/'
    response = api_client.get(url, {'shop_id': shop_id})
    assert response.status_code == status.HTTP_200_OK
    assert any(prod['id'] == product_info.product.id for prod in response.data)