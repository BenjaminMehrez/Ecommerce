from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from taggit.models import Tag
from .models import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse


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



def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    p_images = product.p_images.all

    # Getting all review related to a product
    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    # Getting overage review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    context = {
        'product': product,
        'p_images': p_images,
        'average_rating': average_rating,
        'reviews': reviews,
        'products': products,
    }

    return render(request, 'a_store/product_detail.html', context)


def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, 'a_store/tag.html', context)


def search_view(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'a_store/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = Product.objects.filter(product_status='published').order_by('-id').distinct()
    
    
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    
       
    data = render_to_string('a_store/async/product-list.html', {'products': products} )
    return JsonResponse({'data':data})