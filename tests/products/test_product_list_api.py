import pytest
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
def test_product_list(api_client, product):
    url = reverse('products-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_product_detail(api_client, product):
    url = reverse('products-detail', args=[product.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == product.id


@pytest.mark.django_db
def test_product_detail_not_found(api_client):
    url = reverse('products-detail', args=[9999])
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_product_filter_by_price_and_shop(api_client, product):
    shop2 = baker.make('backend.Shop')
    product2 = baker.make('backend.Product', name='Other')
    baker.make('backend.ProductInfo', product=product, price=100, shop=product.product_info.first().shop)
    baker.make('backend.ProductInfo', product=product2, price=200, shop=shop2)
    url = reverse('products-list')

    response = api_client.get(url, {'min_price': 150})
    assert response.status_code == 200
    assert all(item['id'] == product2.id for item in response.data)

    response = api_client.get(url, {'shop_id': shop2.id})
    assert response.status_code == 200
    assert all(item['id'] == product2.id for item in response.data)


@pytest.mark.django_db
def test_product_search(api_client, product):
    url = reverse('products-list')
    response = api_client.get(url, {'search': product.name[:3]})
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert product.name in [item['name'] for item in response.data]


@pytest.mark.django_db
def test_product_ordering(api_client, product):
    product2 = baker.make('backend.Product', name='Aardvark', model='ZZZ')
    url = reverse('products-list')
    response = api_client.get(url, {'ordering': 'name'})
    assert response.status_code == 200
    assert len(response.data) >= 2
    names = [item['name'] for item in response.data]
    assert names == sorted(names)

