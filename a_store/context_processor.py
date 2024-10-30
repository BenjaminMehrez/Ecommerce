from .models import *

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    return {
        'categories':categories,
        'vendors':vendors,
    }