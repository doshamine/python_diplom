from django.contrib import admin
from .models import (
    Shop, Category, Product, ProductInfo,
    Parameter, ProductParameter, Order, OrderItem, Contact
)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "category")
    search_fields = ("name", "model")
    list_filter = ("category",)
    inlines = [ProductInfoInline]

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "shop", "price", "price_rrc", "quantity")
    list_filter = ("shop",)
    search_fields = ("product__name",)

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ("id", "product_info", "parameter", "value")
    search_fields = ("parameter__name", "value")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "dt", "status")
    list_filter = ("status", "dt")
    search_fields = ("user__username",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "shop", "quantity")
    search_fields = ("order__id", "product__name")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "value")
    search_fields = ("user__username", "value")
    list_filter = ("type",)
