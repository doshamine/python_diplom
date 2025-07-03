import nested_admin
from django.contrib import admin
from django.db import transaction
from django.core.exceptions import ValidationError
from django import forms
from django.forms import BaseInlineFormSet

from .models import (
    Shop, Category, Product, ProductInfo,
    Parameter, ProductParameter, Order, OrderItem, Contact, OrderStatus
)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

class ProductParameterInline(nested_admin.NestedTabularInline):
    model = ProductParameter
    extra = 1

class ProductInfoInline(nested_admin.NestedTabularInline):
    model = ProductInfo
    extra = 1
    inlines = [ProductParameterInline]

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ("id", "name", "model", "category")
    search_fields = ("name", "model")
    list_filter = ("category",)
    inlines = [ProductInfoInline]

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        shop = cleaned_data.get('shop')
        quantity = cleaned_data.get('quantity')

        if product and shop and quantity is not None:
            try:
                product_info = ProductInfo.objects.get(product=product, shop=shop)
            except ProductInfo.DoesNotExist:
                raise ValidationError(
                    f'Товар "{product}" отсутствует в магазине "{shop}".'
                )
            if quantity > product_info.quantity:
                raise ValidationError(
                    f'В наличии только {product_info.quantity} шт. товара "{product}" в магазине "{shop}".'
                )
        return cleaned_data


class OrderItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data.get('product')
                shop = form.cleaned_data.get('shop')
                key = (product, shop)
                if key in seen:
                    raise ValidationError('Нельзя добавлять несколько позиций с одинаковыми товаром и магазином в одном заказе.')
                seen.add(key)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemForm
    formset = OrderItemFormSet
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "dt", "status")
    list_filter = ("status", "dt")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if obj.pk:
            prev_status = Order.objects.get(pk=obj.pk).status
        else:
            prev_status = None
        super().save_model(request, obj, form, change)

        if prev_status != OrderStatus.PAID and obj.status == OrderStatus.PAID:
            with transaction.atomic():
                for item in obj.order_items.all():
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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "value")
    search_fields = ("user__username", "value")
    list_filter = ("type",)
