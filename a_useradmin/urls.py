from django.urls import path
from .views import *


urlpatterns = [
    # Panel
    path('dashboard-admin/', dashboard, name='dashboard-admin'),
    # Products
    path('products/', products, name='products'),
    path('products/<status>/', products_filter, name='products-filter'),
    path('add-products/', add_product, name='add-product'),
    path('edit-products/<pid>/', edit_product, name='edit-product'),
    path('delete-products/<pid>/', delete_product, name='delete-product'),
    # Orders
    path('orders/', orders, name='orders'),
    path('orders/search/', orders_search, name='orders-search'),
    path('orders/<status>/', orders_filter, name='orders-filter'),
    path('order-detail/<id>/', order_detail, name='order-detail'),
    path('change_order_status/<oid>/', change_order_status, name='change-order-status'),
    
    # path('shop_page/', shop_page, name='shop-page'),
    path('reviews/', reviews, name='reviews'),
]