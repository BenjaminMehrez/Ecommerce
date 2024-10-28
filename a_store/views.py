from django.shortcuts import render
from .models import *
# Create your views here.


def home(request):
    products = Product.objects.filter(product_status='published', featured=True)

    context = {
        'products': products
    }

    return render(request, 'a_store/home.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status='published')

    context = {
        'products': products
    }

    return render(request, 'a_store/product_list.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'a_store/category_list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)
    
    context = {
        'category': category,
        'products': products
    }
    
    return render(request, 'a_store/category_product_list.html', context)



def vendor_list_view(request):
    vendors = Vendor.objects.all()
    
    context = {
        'vendors': vendors
    }
    return render(request, 'a_store/vendor_list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')
    
    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'a_store/vendor_detail.html', context)