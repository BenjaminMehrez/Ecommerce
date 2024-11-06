from .models import *
from django.db.models import Min, Max
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    try:
        wishlist =  Wishlist.objects.filter(user=request.user)
    except:
        wishlist =  0
          
    
    return {
        'categories':categories,
        'wishlist':wishlist,
        'vendors':vendors,
        'min_max_price':min_max_price,
    }