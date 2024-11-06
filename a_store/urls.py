from django.urls import path, include
from .views import *


urlpatterns = [
    # Paypal
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment-success/', payment_success_view, name='payment-success'),
    path('payment-failed/', payment_failed_view, name='payment-failed'),
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
    path('checkout/', checkout_view, name='checkout'),
    # Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'),
    path('make-default-address/', make_address_default, name='make-default-address'),
    # Order Detail
    path('dashboard/order/<int:id>/', order_datail, name='order-detail'),
    # Wishlist
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    path('delete-wishlist/', delete_wishlist, name='delete-wishlist'),
    
    
]
