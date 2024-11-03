from django.urls import path, include
from .views import *


urlpatterns = [
    # Homepage
    path('', home, name='home'),
    path('products/', product_list_view, name='product-list'),
    path('product/<pid>/', product_detail_view, name='product-detail'),
    # Category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    # Vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    # Tags
    path('products/tag/<slug:tag_slug>/', tag_list_view, name='tags'),
    # Search
    path('search/', search_view, name='search'),
    # Filter
    path('filter-products/', filter_product, name="filter-product"),
    # Cart
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('delete-from-cart/', delete_item_from_cart, name='delete-from-cart'),
    path('update-cart/', update_cart, name='update-cart'),
    # Checkout
    path('checkout/', checkout_view, name='checkout')
]
