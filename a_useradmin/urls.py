from django.urls import path
from .views import *


urlpatterns = [
    path('dashboard-admin/', dashboard, name='dashboard-admin'),
    path('products/', products, name='products'),
    path('add-products/', add_product, name='add-product'),
    path('edit-products/<pid>/', edit_product, name='edit-product'),
    path('delete-products/<pid>/', delete_product, name='delete-product'),
    path('orders/', orders, name='orders'),
    path('order-detail/<id>/', order_detail, name='order-detail'),
    path('change_order_status/<oid>/', change_order_status, name='change-order-status'),
]