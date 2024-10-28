from django.urls import path, include
from .views import *


urlpatterns = [
    # homepage
    path('', home, name='home'),
    path('products/', product_list_view, name='product-list'),
    path('product/<pid>/', product_detail_view, name='product-detail'),
    # category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    # vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    
]
