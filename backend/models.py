from django.contrib.auth.models import User
from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='name', unique=True)
    url = models.URLField(verbose_name='url', unique=True)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.BigIntegerField(verbose_name='id', primary_key=True)
    name = models.CharField(max_length=50, verbose_name='name')
    shops = models.ManyToManyField(Shop, verbose_name='shops', related_name='categories')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigIntegerField(verbose_name='id', primary_key=True)
    category = models.ForeignKey(Category, verbose_name='category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='name')
    model = models.CharField(max_length=100, verbose_name='model')
    shops = models.ManyToManyField(Shop, verbose_name='shops', related_name='products', through='ProductInfo')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='product', related_name='product_info', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='shop', related_name='product_info', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price_rrc')
    quantity = models.IntegerField(verbose_name='quantity')

class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='name', unique=True)

    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'
        ordering = ['name']

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='product_info', related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='parameter', related_name='product_parameters', on_delete=models.CASCADE)
    value = models.TextField(verbose_name='value')

class OrderStatus(models.TextChoices):
    NEW = 'new', 'New'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped'
    CANCELED = 'canceled', 'Canceled'

class Order(models.Model):
    user = models.ForeignKey(
        User, verbose_name='user',
        related_name='orders',
        on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, verbose_name='status',
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['dt']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='order', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', related_name='order_items', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='shop', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='quantity')


class ContactType(models.TextChoices):
    ADDRESS = 'address', 'адрес'
    EMAIL = 'email', 'почта'
    PHONE = 'phone', 'телефон'
    TELEGRAM = 'telegram', 'телеграм'


class Contact(models.Model):
    type = models.CharField(max_length=50, verbose_name='type', choices=ContactType.choices)
    user = models.ForeignKey(User, verbose_name='user', related_name='contacts', on_delete=models.CASCADE)
    value = models.CharField(max_length=100, verbose_name='value')

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['type']
