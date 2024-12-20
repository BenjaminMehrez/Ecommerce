from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from a_store.models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q


# Create your views here.



def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum('price'))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('-id')
    latest_orders = CartOrder.objects.all().order_by('-order_date')
    
    this_month = datetime.datetime.now().month
    
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum('price'))
    
    context = {
    'revenue': revenue,
    'total_orders_count': total_orders_count,
    'all_products': all_products,
    'all_categories': all_categories,
    'new_customers': new_customers,
    'latest_orders': latest_orders,
    'this_month': this_month,
    'monthly_revenue': monthly_revenue,
    }
    
    return render(request, 'a_useradmin/dashboard.html', context)



@user_passes_test(admin_required)
def products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
    'all_products': all_products,
    'all_categories': all_categories,
    }
    
    return render(request, 'a_useradmin/products.html', context)
    

@user_passes_test(admin_required)
def products_filter(request, status):
    if status == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_status=status)
    all_products = Product.objects.values('product_status').distinct()
    
    context = {
    'products': products,
    'all_products': all_products,
    }
    
    return render(request, 'a_useradmin/products_filter.html', context)
    
    
@user_passes_test(admin_required)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        
        # Crear un formset para los talles
        ProductSizeFormSet = modelformset_factory(ProductSize, form=ProductSizeForm, extra=5)  # 'extra=1' permite agregar un formulario vacío
        formsize = ProductSizeFormSet(request.POST)
        
        if form.is_valid() and formsize.is_valid():
            # Guardar el producto principal
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()

            # Guardar todos los talles asociados al producto
            for size_form in formsize:
                if size_form.is_valid():
                    size = size_form.save(commit=False)
                    size.product = new_product
                    size.save()
                    
            # Procesar las imágenes adicionales
            images = request.FILES.getlist('images')  # Obtener la lista de imágenes
            for image in images:
                ProductImages.objects.create(product=new_product, images=image)

            form.save_m2m()  # Guardar relaciones Many-to-Many
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('products')
    else:
        form = AddProductForm()
        ProductSizeFormSet = modelformset_factory(ProductSize, form=ProductSizeForm, extra=5)  # Formulario vacío adicional
        formsize = ProductSizeFormSet(queryset=ProductSize.objects.none()) 

    context = {'form': form, 'formsize': formsize}
    return render(request, 'a_useradmin/add_product.html', context)



@user_passes_test(admin_required)
def edit_product(request, pid):
    # Obtener el producto a editar
    product = get_object_or_404(Product, pid=pid)
    
    if request.method == 'POST':
        # Cargar el formulario del producto con los datos POST y los archivos
        form = AddProductForm(request.POST, request.FILES, instance=product)
        
        # Crear un formset para los talles existentes del producto
        ProductSizeFormSet = modelformset_factory(ProductSize, form=ProductSizeForm, extra=0)
        formsize = ProductSizeFormSet(request.POST, queryset=ProductSize.objects.filter(product=product))
        
        if form.is_valid() and formsize.is_valid():
            # Guardar el producto principal
            updated_product = form.save(commit=False)
            updated_product.user = request.user
            updated_product.save()
            
            # Guardar o eliminar los talles asociados al producto
            for size_form in formsize:
                size = size_form.save(commit=False)
                size.product = updated_product
                size.save()

            # Procesar las imágenes adicionales
            images = request.FILES.getlist('images')  # Obtener la lista de imágenes
            for image in images:
                ProductImages.objects.create(product=updated_product, images=image)

            form.save_m2m()  # Guardar relaciones Many-to-Many
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('products')
    else:
        # Crear el formulario para el producto existente
        form = AddProductForm(instance=product)
        
        # Crear un formset para los talles existentes
        ProductSizeFormSet = modelformset_factory(ProductSize, form=ProductSizeForm, extra=0)
        formsize = ProductSizeFormSet(queryset=ProductSize.objects.filter(product=product))
    
    context = {'form': form, 'formsize': formsize}
    return render(request, 'a_useradmin/edit_product.html', context)




@user_passes_test(admin_required)
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto Eliminado')
        return redirect('products')
    
    
    return render(request, 'a_useradmin/delete_product.html', {'product': product})


@user_passes_test(admin_required)
def orders(request):
    orders = CartOrder.objects.all().order_by('-order_date')
    context = {
        'orders': orders
    }
    
    return render(request, 'a_useradmin/orders.html', context)


@user_passes_test(admin_required)
def orders_filter(request, status):
    if status == "all":
        orders = CartOrder.objects.all().order_by('-order_date')
    elif status == 'True' or status == 'False':
        orders = CartOrder.objects.filter(paid_status=status).order_by('-order_date')
    else:
        orders = CartOrder.objects.filter(product_status=status).order_by('-order_date')
        
    all_orders = CartOrder.objects.values('product_status').distinct()
    
    context = {
        'orders': orders,
        'all_orders': all_orders,
    }
    
    return render(request, 'a_useradmin/orders_filter.html', context)


@user_passes_test(admin_required)
def orders_search(request):
    query = request.GET.get('qorder')
    
    if query:
        orders = CartOrder.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(oid__icontains=query))
    else:
        orders = CartOrder.objects.all()
    
    context = {
        'orders': orders,
        'query': query,
    }
    
    return render(request, 'a_useradmin/search.html', context)


@user_passes_test(admin_required)
def order_detail(request, id):
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order_items': order_items,
        'order': order
    }
    
    return render(request, 'a_useradmin/order_detail.html', context)



@user_passes_test(admin_required)
def change_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.product_status = status
        order.save()
        messages.success(request, f'El estado de orden fue cambiado a {status}')
        
    return redirect('order-detail-admin', order.id)



# def shop_page(request):
#     products = Product.objects.all()
#     revenue = CartOrder.objects.aggregate(price=Sum('price'))
#     total_sales = CartOrderItems.objects.filter(order__paid_status=True).aggregate(qty=Sum("qty"))
    
#     context = {
#         'products': products,
#         'revenue': revenue,
#         'total_sales': total_sales,
#     }
    
#     return render(request, 'a_useradmin/shop_page.html', context)


def reviews(request):
    reviews = ProductReview.objects.all().order_by('-date')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'a_useradmin/reviews.html', context)