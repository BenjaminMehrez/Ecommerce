from django.urls import path, include
from .views import *


urlpatterns = [
    # Payment
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment-success/<oid>/', payment_success_view, name='payment-success'),
    path('payment-failed/', payment_failed_view, name='payment-failed'),
    path('payment-notification/', payment_notification, name='payment_notification'),
    
    # Homepage, Products
    path('', home, name='home'),
    path('products/', product_list_view, name='product-list'),
    path('product/<pid>/', product_detail_view, name='product-detail'),
    
    # Contact
    path('contact/', contact, name='contact'),
    path('ajax-contact-form/', ajax_contaxt, name='ajax-contaxt'),
    
    # Category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    
    # Vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    
    # Tags
    path('products/tag/<slug:tag_slug>/', tag_list_view, name='tags'),
    
    # Reviews
    path('ajax-add-review/<int:pid>/', ajax_add_review, name='ajax-add-review'),
    
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
    path('checkout/<oid>/', checkout, name='checkout'),
    path('save-checkout-info/', save_checkout_info, name='save-checkout-info'),
    
    # Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'),
    
    # Dashboard Addresss
    path('make-default-address/', make_address_default, name='make-default-address'),
    path('dashboard-address/', customer_dashboard_address, name='dashboard-address'),
    
    # Dashboard Profile
    path('dashboard-profile/', customer_dashboard_profile, name='dashboard-profile'),
    
    # Dashboard Orders
    path('dashboard-orders/', customer_dashboard_orders, name='dashboard-orders'),
    
    # Order Detail
    path('dashboard/order/<int:id>/', order_datail, name='order-detail'),
    
    # Wishlist
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    path('delete-wishlist/', delete_wishlist, name='delete-wishlist'),
    
    # COOKIES
    path('cookies-settings/', cookies_settings, name='cookies-settings'),
    
    # OTHERS
    path('terms-of-service/', terms_of_service, name='terms-of-service'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    

]
