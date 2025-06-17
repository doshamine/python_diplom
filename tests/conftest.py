import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = baker.make('auth.User', username='testuser')
    Token.objects.get_or_create(user=user)
    return user

@pytest.fixture
def auth_client(api_client, user):
    token = Token.objects.get(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client

@pytest.fixture
def product():
    return baker.make('backend.Product')

@pytest.fixture
def shop():
    return baker.make('backend.Shop')

@pytest.fixture
def order(user):
    return baker.make('backend.Order', user=user)

@pytest.fixture
def order_item(order, product, shop):
    return baker.make('backend.OrderItem', order=order, product=product, shop=shop, quantity=1)