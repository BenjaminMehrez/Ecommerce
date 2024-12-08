from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Avg, Count
from taggit.models import Tag
from .models import *
import json
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from a_users.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import calendar
from django.db.models.functions import ExtractMonth
from django.core import serializers
from .forms import *
from .mercadopago import create_preference
from django.http import HttpResponse
from django.core.paginator import Paginator
import mercadopago



# Create your views here.


def home(request):
    products = Product.objects.filter(product_status='publicado', featured=True).order_by('-date')


    paginator = Paginator(products, 8)
    page = int(request.GET.get('page', 1))
    
    try:
        products = paginator.page(page)
    except:
        return HttpResponse('')


    context = {
        'products': products,
        'page': page,
    }
    
    if request.htmx:
        return render(request, 'snippets/loop_home_products.html', context)

    return render(request, 'a_store/home.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status='publicado').order_by('-date')

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
    products = Product.objects.filter(product_status='publicado', category=category).order_by('-date')
    
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
    products = Product.objects.filter(vendor=vendor, product_status='publicado').order_by('-date')

    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'a_store/vendor_detail.html', context)



def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:5]
    
    try:
        wishlist_items = Wishlist.objects.filter(user=request.user)  # Obtener la lista de deseos del usuario actual
        wishlist_product_ids = wishlist_items.values_list('product_id', flat=True)
    except:
        wishlist_product_ids = 0
        
    # Getting all review related to a product
    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    # Getting overage review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    # Product Review form
    review_form = ProductReviewForm()
    
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False
    
    
    p_image = product.p_images.all()
    p_size = product.sizes.all()
    
    context = {
        'product': product,
        'p_image': p_image,
        'p_size': p_size,
        'review_form': review_form,
        'average_rating': average_rating,
        'make_review': make_review,
        'reviews': reviews,
        'products': products,
        'wishlist_product_ids': wishlist_product_ids,
    }

    return render(request, 'a_store/product_detail.html', context)


def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter(product_status='publicado').order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, 'a_store/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review= request.POST['review'],
        rating= request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating']
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse({
        'bool': True,
        'context': context,
        'average_reviews': average_reviews,
    })


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
    
    print('max', max_price)
    print('min', min_price)
    
    products = Product.objects.filter(product_status='publicado').order_by('-id').distinct()
    
    
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
    
    cart_key = f"{request.GET['id']}-{request.GET['size']}"
            
    cart_product[cart_key] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'size': request.GET['size'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        if cart_key in cart_data:
            cart_data[cart_key]['qty'] += int(cart_product[cart_key]['qty'])
            request.session['cart_data_obj'] = cart_data
            return JsonResponse({
                'success': False,
                'message': 'El producto ya está en el carrito. Se actualizó la cantidad.',
                'totalcartitems': len(cart_data)
            })
        
        cart_data.update(cart_product)
        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        # Iterar sobre los productos del carrito
        for p_key, item in cart_data.items():
            # Sumar precio total basado en cantidad y precio unitario
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        # Renderizar la plantilla del carrito
        return render(request, 'a_store/cart.html', {
            'cart_data': cart_data,  # Pasar todos los datos del carrito
            'totalcartitems': len(cart_data),  # Cantidad total de productos únicos
            'cart_total_amount': cart_total_amount  # Monto total del carrito
        })
    else:
        # Si no hay productos, redirigir al home con un mensaje
        messages.warning(request, 'No hay productos en el carrito.')
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


@login_required
def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        number = request.POST.get('number')
        zipcode = request.POST.get('zipcode')
        level = request.POST.get('level')
        departament = request.POST.get('departament')
        city = request.POST.get('city')
        country = request.POST.get('country')
        mobile = request.POST.get('mobile') 
        
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['address'] = address
        request.session['number'] = number
        request.session['zipcode'] = zipcode
        request.session['level'] = level
        request.session['departament'] = departament
        request.session['city'] = city
        request.session['country'] = country
        request.session['mobile'] = mobile
        
        
        if 'cart_data_obj' in request.session:
            
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
            
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                number=number,
                zipcode=zipcode,
                level=level,
                departament=departament,
                city=city,
                country=country,
                phone=mobile,
            ) 
            
            del request.session['first_name']
            del request.session['last_name']
            del request.session['email']
            del request.session['address']
            del request.session['number']
            del request.session['zipcode']
            del request.session['level']
            del request.session['departament']
            del request.session['city']
            del request.session['country']
            del request.session['mobile']
            
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                cart_order_products = CartOrderItems.objects.create(
                    order=order,
                    invoice_no='INVOICE_NO-' + str(order.id), # INVOICE NO
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    size=item['size'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
                )
            
        return redirect('checkout', order.oid)       
    return redirect('cart')       



@login_required
def checkout(request, oid):
    public_key = settings.MERCADO_PAGO_PUBLIC_KEY
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, 'Cupon ya fue aplicado')
                return redirect('checkout', order.oid)
            else:
                discount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()
                
                messages.success(request, 'Cupon aplicado')
                return redirect('checkout', order.oid)
        else:
            messages.warning(request, 'No existe el cupon')
            return redirect('checkout', order.oid)
    
    preference = create_preference(order)
    
    context = {
        'order':order,
        'order_items': order_items,
        'public_key': public_key,
        'preference_id': preference['id'],
        'init_point': preference['init_point']
    }

    
    return render(request, 'a_store/checkout.html', context)


@csrf_exempt
def payment_notification(request):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    if request.method == "POST":
        try:
            # Cargar la notificación enviada por Mercado Pago
            data = json.loads(request.body)
            payment_id = data.get("data", {}).get("id")  # ID del pago

            # Consultar los detalles del pago usando el SDK de Mercado Pago
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info.get("response")

            if payment:
                payment_status = payment.get("status")
                external_reference = payment.get("external_reference")  # Obtener la referencia externa

                # Buscar la orden correspondiente
                order = CartOrder.objects.get(oid=external_reference)

                # Actualizar el estado de la orden según el estado del pago
                if payment_status == "approved":
                    order.paid_status = True
                elif payment_status in ["rejected", "cancelled"]:
                    order.paid_status = False
                elif payment_status == "pending":
                    order.paid_status = False  # Pendiente

                # Guardar la orden con la actualización del estado
                order.save()

            # Responder con un JSON que confirma la recepción
            return JsonResponse({"status": "success"})

        except Exception as e:
            print(f"Error al procesar la notificación: {e}")
            return JsonResponse({"status": "error"}, status=400)

    return JsonResponse({"status": "error"}, status=400)


def payment_success_view(request, oid):
    try:
        order = CartOrder.objects.get(oid=oid)

        # Verificar el estado del pago directamente desde Mercado Pago
        payment_id = request.GET.get("payment_id")  # Obteniendo el ID del pago
        if not payment_id:
            raise ValueError("No se encontró el ID de pago.")

        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        # Obtener detalles del pago
        payment_info = sdk.payment().get(payment_id)

        # Aquí podría estar el problema
        if payment_info["status"] != 200:
            raise ValueError(f"Error validando el pago: {payment_info}")

        payment_status = payment_info["response"]["status"]
        if payment_status != "approved":
            raise ValueError(f"Pago no aprobado: {payment_status}")

        # Actualizar la orden como pagada
        if not order.paid_status:
            if 'cart_data_obj' in request.session:
                del request.session['cart_data_obj']
            order.paid_status = True
            order.save()
            

        return render(request, 'a_store/payment_success.html', {'order': order})

    except Exception as e:
        print(f"Error validando el pago: {e}")
        return render(request, 'a_store/payment_failed.html', {'error': str(e)})
    

def payment_failed_view(request):
    return render(request, 'a_store/payment_failed.html')


@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')
    month = []
    total_orders = []
    
    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])
    
    context = {
        'orders':orders,
        'month': month,
        'total_orders': total_orders,
    }
    return render(request, 'a_store/dashboard.html', context)
    
    
@login_required
def customer_dashboard_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'profile': profile
    }
    
    return render(request, 'a_store/dashboard_profile.html', context)
    
    
@login_required
def customer_dashboard_orders(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
        
    context = {
        'orders_list': orders_list
    }
    
    return render(request, 'a_store/dashboard_orders.html', context)
    
    
@login_required
def customer_dashboard_address(request):
    address = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        number = request.POST.get('number')
        zipcode = request.POST.get('zipcode')
        level = request.POST.get('level')
        departament = request.POST.get('departament')
        city = request.POST.get('city')
        country = request.POST.get('country')
        mobile = request.POST.get('mobile')
            
        new_address = Address.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            number=number,
            zipcode=zipcode,
            level=level,
            departament=departament,
            city=city,
            country=country,
            mobile=mobile,
        )
        messages.success(request, 'Direccion Agregada')
        return redirect('dashboard-address')
            
        
    context = {
        'address': address,

    }
    
    return render(request, 'a_store/dashboard_address.html', context)
    

    
@login_required
def order_datail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    
    context = {
        'order_items': order_items,
        'order': order,
    }
    return render(request, 'a_store/order-detail.html', context)



@login_required
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean': True})




@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.all()
    
    context = {
        'wishlist': wishlist,
    }
    
    return render(request, 'a_store/wishlist.html', context)


@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    
    context = {}
    
    wishlist_count =  Wishlist.objects.filter(product=product, user=request.user).count()
    
    if wishlist_count > 0:
        context = {
            'bool': True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            'bool': True
        }
    
    return JsonResponse(context)


@login_required
def delete_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    product = Wishlist.objects.get(id=pid)
    product.delete()
    
    context = {
        'bool': True,
        'wishlist': wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string('a_store/async/wishlist-list.html', context)
    return JsonResponse({'data': data, 'w': wishlist_json})



def contact(request):
    return render(request, 'a_store/contact.html')


def ajax_contaxt(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContacUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message
    )

    
    data = {
        'bool': True,
        'message': 'Mensaje enviado exitosamente'
    }
    
    return JsonResponse({'data': data})


def cookies_settings(request):
    return render(request, 'a_store/cookies_settings.html')

def terms_of_service(request):
    return render(request, 'a_store/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'a_store/privacy_policy.html')




def about_us(request):
    pass


def purchase_guide(request):
    pass

