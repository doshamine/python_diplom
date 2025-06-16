from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Product, Shop, ProductInfo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url']

class ProductInfoSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = ProductInfo
        fields = ['shop', 'price', 'price_rrc', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'product_info']

