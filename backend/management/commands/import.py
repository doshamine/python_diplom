import os.path

import yaml
from django.core.management import BaseCommand

from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        shop_num = 1
        while os.path.exists(f'data/shop{shop_num}.yaml'):
            with open(f'data/shop{shop_num}.yaml', 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            shop_num += 1

            shop = Shop(name=data['shop'])
            shop.save()

            for category in data['categories']:
                category = Category(id=category['id'], name=category['name'])
                category.save()
                category.shops.add(shop)

            for product in data['products']:
                category, _ = Category.objects.get_or_create(id=product['category'])
                product = Product(
                    id=product['id'], name=product['name'],
                    model=product['model'], category=category
                )
                product.save()

                product_info = ProductInfo(
                    shop=shop, product=product, price=product['price'],
                    price_rrc=product['price_rrc'], quantity=product['quantity']
                )
                product_info.save()

                for parameter, value in product['parameters'].items():
                    parameter = Parameter(name=parameter)
                    parameter.save()

                    product_parameter = ProductParameter(
                        product_info=product_info,
                        parameter=parameter,
                        value=value
                    )
                    product_parameter.save()

