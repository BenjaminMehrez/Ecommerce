from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from a_store.models import *
from .forms import *
from django.contrib import messages

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
    latest_orders = CartOrder.objects.all()
    
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
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            
            messages.success(request, 'Producto Agregado')
            return redirect('products')
    else:
        form = AddProductForm()
        
    
    context = {
        'form': form
    }
    
    return render(request, 'a_useradmin/add_product.html', context)



@user_passes_test(admin_required)
def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            
            messages.success(request, 'Producto Actualizado')
            return redirect('products')
    else:
        form = AddProductForm(instance=product)
        
    
    context = {
        'form': form
    }
    
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
    orders = CartOrder.objects.all()
    context = {
        'orders': orders
    }
    
    return render(request, 'a_useradmin/orders.html', context)


def order_detail(request, id):
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order_items': order_items,
        'order': order
    }
    
    return render(request, 'a_useradmin/order_detail.html', context)