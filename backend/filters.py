import django_filters
from backend.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='product_info__price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='product_info__price', lookup_expr='lte')
    shop_id = django_filters.NumberFilter(field_name='product_info__shop__id')

    class Meta:
        model = Product
        fields = ['category', 'shop_id', 'min_price', 'max_price']
