from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as authlogin, logout
from django.contrib.auth.models import User
from category_app.models import Paint, Art
from product_app.models import Product
from variant_app.models import Variant
from django.shortcuts import get_object_or_404
from django.contrib import messages

#---------------- ADMIN LOGIN SECTION --------------#

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                authlogin(request, user)
                return redirect('panel')
            else:
                return render(request, 'admin/log.html')
        else:
            return render(request, 'admin/log.html')

    return render(request, 'admin/log.html')


def admin_logout(request):
    logout(request)
    return redirect('login_admin')

def panel(request):
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    return render(request, 'admin/dashboard.html')


#----------------- ADD PRODUCT SECTION ---------------#

def productadd(request):
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    paint = Paint.objects.filter(paint_type_status = True)
    art = Art.objects.filter(art_type_status = True)

    if not paint.exists() and not art.exists():
        messages.warning(request, "No available Paint or Art items found.")
    context = {
        'paints': paint,
        'arts' : art
    }
    return render(request,'admin/productadd.html', context)

def product(request):
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    paint = Paint.objects.all()
    art = Art.objects.all()
    products = Product.objects.all().order_by('-id')
    return render(request,'admin/product.html',{'products':products, 'paint':paint, 'art':art})


#------------------- USERS SECTION ----------------#

def users(request):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')

    users = User.objects.filter(is_staff = False).order_by('id')
    return render(request,'admin/users.html', {'users':users})

def user_status(request,user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin') 

    user = get_object_or_404(User,id = user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('users')


#------------------ CATEGORY SECTION ----------------#

def art(request):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    art_type = Art.objects.all().order_by('id')
    return render(request,'admin/art.html',{'art_type':art_type})

def paint(request):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    paint_type = Paint.objects.all().order_by('id')
    return render(request,'admin/paint.html',{'paint_type': paint_type})


#---------------- VARIANTS SECTION ---------------#

def variant(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    products = get_object_or_404(Product, id = product_id)
    variants=Variant.objects.filter(product=products)
    
    if request.method == 'POST':
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        size = request.POST.get('size')

        Variant.objects.create(
            frame_size=size,
            stock=stock,
            price=price,
            product=products
        )
        return redirect('variant', product_id=products.id)

    return render(request,'admin/variant.html', {'variants' : variants})

# def orders(request):
#     return render(request,'admin/orders.html')
