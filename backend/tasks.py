import os
import yaml
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


@shared_task
def send_mail_task(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def do_import():
    shop_num = 1
    while os.path.exists(f'data/shop{shop_num}.yaml'):
        with open(f'data/shop{shop_num}.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        shop_num += 1

        shop = Shop(name=data['shop'], url=data['url'])
        shop.save()

        for category_data in data['categories']:
            category, _ = Category.objects.get_or_create(id=category_data['id'], name=category_data['name'])
            category.shops.add(shop)
            category.save()

        for product_data in data['products']:
            category = Category.objects.get(id=product_data['category'])
            product, _ = Product.objects.get_or_create(
                id=product_data['id'], name=product_data['name'],
                model=product_data['model'], category=category
            )
            product.save()

            product_info = ProductInfo(
                shop=shop, product=product, price=product_data['price'],
                price_rrc=product_data['price_rrc'], quantity=product_data['quantity']
            )
            product_info.save()

            for parameter_name, value in product_data['parameters'].items():
                parameter, _ = Parameter.objects.get_or_create(name=parameter_name)

                product_parameter = ProductParameter(
                    product_info=product_info,
                    parameter=parameter,
                    value=value
                )
                product_parameter.save()