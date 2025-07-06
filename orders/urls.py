"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from backend.views import RegisterView, ProductViewSet, OrderViewSet, ContactViewSet, OrderConfirmAPIView, CartAPIView, \
    import_view

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'contacts', ContactViewSet, basename='contacts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import/', import_view, name='import'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', obtain_auth_token, name='login'),
    path('api/v1/confirm/', OrderConfirmAPIView.as_view(), name='confirm'),
    path('api/v1/cart/', CartAPIView.as_view(), name='cart'),
    path('_nested_admin/', include('nested_admin.urls')),
    path('api/v1/', include(router.urls))
]