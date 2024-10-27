from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list_view, name='product-list'),
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>', category_product_list_view, name='category-product-list'),
]
