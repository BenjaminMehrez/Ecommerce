from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Avg
from taggit.models import Tag
from .models import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages


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



def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])])['qty']
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'a_store/cart.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, 'no hay productos')
        return redirect('home')


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
        
    context = render_to_string('a_store/async/cart-list.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])})





def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
        
    context = render_to_string('a_store/async/cart-list.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])})



def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    return render(request, 'a_store/checkout.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
