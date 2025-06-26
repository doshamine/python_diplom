from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from backend.models import Order, OrderStatus, ProductInfo


@receiver(pre_save, sender=Order)
def save_previous_status(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        instance._previous_status = previous.status
    else:
        instance._previous_status = None


@receiver(post_save, sender=Order)
def decrease_stock_on_paid(sender, instance, created, **kwargs):
    previous_status = getattr(instance, '_previous_status', None)
    if previous_status != OrderStatus.PAID and instance.status == OrderStatus.PAID:
        for item in instance.order_items.all():
            try:
                product_info = ProductInfo.objects.select_for_update().get(
                    product=item.product,
                    shop=item.shop
                )
            except ProductInfo.DoesNotExist:
                raise ValidationError(
                    f'Товар "{item.product}" отсутствует в магазине "{item.shop}".'
                )

            if product_info.quantity < item.quantity:
                raise ValidationError(
                    f'Недостаточно товара "{item.product}" в магазине "{item.shop}". В наличии: {product_info.quantity}.'
                )

            product_info.quantity -= item.quantity
            product_info.save()
