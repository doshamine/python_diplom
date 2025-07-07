import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from orders.settings import DEFAULT_FROM_EMAIL

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = baker.make('auth.User', username='testuser', email=DEFAULT_FROM_EMAIL)
    Token.objects.get_or_create(user=user)
    return user

@pytest.fixture
def auth_client(api_client, user):
    token = Token.objects.get(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client

@pytest.fixture
def product():
    product = baker.make('backend.Product')
    shop = baker.make('backend.Shop')
    baker.make('backend.ProductInfo', product=product, shop=shop, price=100)
    return product

@pytest.fixture
def shop():
    return baker.make('backend.Shop')

@pytest.fixture
def order(user):
    return baker.make('backend.Order', user=user)

@pytest.fixture
def order_item(order, product, shop):
    return baker.make('backend.OrderItem', order=order, product=product, shop=shop, quantity=1)