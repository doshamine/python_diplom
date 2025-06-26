from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Product, Shop, ProductInfo, OrderItem, Order, Contact


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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'shop', 'quantity']

    def validate(self, data):
        product = data.get('product')
        shop = data.get('shop')
        quantity = data.get('quantity')

        try:
            product_info = ProductInfo.objects.get(product=product, shop=shop)
        except ProductInfo.DoesNotExist:
            raise serializers.ValidationError(
                f'Товар "{product}" отсутствует в магазине "{shop}".'
            )

        if quantity > product_info.quantity:
            raise serializers.ValidationError(
                f'Недостаточно товара "{product}" в магазине "{shop}". В наличии: {product_info.quantity}.'
            )

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'dt', 'status', 'order_items']
        read_only_fields = ['user', 'dt']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type', 'value']