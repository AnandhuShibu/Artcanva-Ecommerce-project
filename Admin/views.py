from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as authlogin, logout
from django.contrib.auth.models import User
from coupon_app.models import Coupons
from category_app.models import Paint, Art
from product_app.models import Product
from variant_app.models import Variant
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from User.models import Order,Order_details,Address

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
    search_query = request.GET.get('q', '').strip()  # Get search query, default to an empty string

    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    paint = Paint.objects.all()
    art = Art.objects.all()
    products = Product.objects.all().order_by('-id')

    if search_query:
        products = products.filter(product_name__icontains=search_query)
    

    paginator = Paginator(products, 7)  # Show 10 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the corresponding page

    no_products_found = not products.exists()

    context = {
        'paint':paint,
        'art':art,
        'page_obj': page_obj,
        'search_query': search_query,
        'no_products_found': no_products_found,
    }
    return render(request,'admin/product.html', context)


#------------------- USERS SECTION ----------------#

def users(request):
    search_query = request.GET.get('q', '').strip()
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    
    users = User.objects.filter(is_staff = False).order_by('id')

    if search_query:
        users = users.filter(username__icontains=search_query)
    no_user_found = not users.exists()

    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'admin/users.html', {'page_obj': page_obj, 'no_user_found': no_user_found})


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
    search_query = request.GET.get('q', '').strip()
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    art_type = Art.objects.all().order_by('id')

    if search_query:
        art_type = art_type.filter(art_type__icontains=search_query)

    paginator = Paginator(art_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    no_art_found = not art_type.exists()

    return render(request,'admin/art.html',{'page_obj':page_obj, 'no_art_found': no_art_found})


def paint(request):
    search_query = request.GET.get('q', '').strip()
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    paint_type = Paint.objects.all().order_by('id')
    if search_query:
        paint_type = paint_type.filter(paint_type__icontains=search_query)
    paginator = Paginator(paint_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    no_paint_found = not paint_type.exists()

    return render(request,'admin/paint.html',{'page_obj': page_obj, 'no_paint_found': no_paint_found})


#---------------- VARIANTS SECTION ---------------#

def variant(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    
    products = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(product=products).order_by('-id')

    if request.method == 'POST':
        # Check if it's an edit or a new variant
        variant_id = request.POST.get('variant_id')
        
        size = request.POST.get('size')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if variant_id:  # If variant_id exists, update the variant
            variant = get_object_or_404(Variant, id=variant_id)
            variant.frame_size = size
            variant.price = price
            variant.stock = stock
            variant.save()
        else: 
            existing_variant = Variant.objects.filter(product=products, frame_size=size).first()
            if existing_variant:
                # Handle the case where the variant already exists
                # You can return an error message to the template or use messages framework
                return render(request, 'admin/variant.html', {
                    'page_obj': variants,
                    'error_message': "!"
                })
            
             # Otherwise, create a new variant
            Variant.objects.create(
                frame_size=size,
                stock=stock,
                price=price,
                product=products
            )
        
        return redirect('variant', product_id=products.id)
    

    paginator = Paginator(variants, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    return render(request, 'admin/variant.html', {'page_obj': page_obj})





#-------------------- ORDERS SECTION -----------------#

def all_orders(request):
    orders = Order.objects.all().order_by('-id')

    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,'admin/orders.html', {'page_obj': page_obj})


def order_items(request,order_id):
    order_id = get_object_or_404(Order, id = order_id)
    total_amount=order_id.total_amount
    order_items=Order_details.objects.filter(order=order_id)
    order_address=Address.objects.get(id=order_id.address.id)
    print(order_address)
    print(total_amount)
    print(order_items)
    context={
        'order_items':order_items,
        'order_address':order_address,
        'total_amount':total_amount,
        'order_id':order_id    
    }
    return render(request,'admin/order_items.html', context)


def change_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        return redirect('order_items', order_id=order_id)


#----------------- COUPONS SECTION --------------#



def coupon(request):
    search_query = request.GET.get('q', '').strip()
    coupons = Coupons.objects.all()
    print('hii')
    if search_query:
        coupons = coupons.filter(coupon_code__icontains=search_query)
        print('working')
    
    paginator = Paginator(coupons, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    no_coupon_found = not coupons.exists()

    return render(request,'admin/coupons.html', {'page_obj': page_obj, 'no_coupon_found': no_coupon_found})

def remove_coupon(request, coupon_id):
    print("hhhgh")
    coupon_item = Coupons.objects.get(id = coupon_id)
    coupon_item.delete()    
    return redirect('coupon')


def edit_coupon(request):
    coupon_id = request.POST.get('categoryId')
    edit_coupon = request.POST.get('edit_coupon').strip()
    percentage = request.POST.get('percentage').strip()
    expiry_date = request.POST.get('expiry_date').strip()
    coupon = get_object_or_404(Coupons, id = coupon_id)

    print(coupon_id)

    
    if len(edit_coupon) > 6:
        messages.error(request, "Paint type cannot exceed 6 characters.")
        return redirect('coupon')
    
    Coupons.coupon_code=edit_coupon
    Coupons.save()
    messages.success(request, "Success")
    return redirect('coupon')







def add_coupon(request):
    print('hai jaseeeeeeeeeeeeer')
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code').strip().upper()
        percentage = request.POST.get('percentage').strip()
        expiry_date = request.POST.get('expiry_date').strip()

        print(coupon_code)
        print(percentage)
        print(expiry_date)
        
        all_coupons = [coupon.coupon_code for coupon in Coupons.objects.all()]

        if coupon_code in all_coupons:
            messages.error(request, "Coupon already exists.")
            return redirect('coupon')
        
        for existing_coupon in all_coupons:
            if coupon_code in existing_coupon:
                messages.error(request, f"coupon '{coupon_code}' is too similar to '{existing_coupon}'.")
                return redirect('coupon')


        if Coupons.objects.filter(coupon_code=coupon_code).exists():
            messages.error(request, "Coupon already exists.")
            return redirect('coupon')
        
        if len(coupon_code) < 6:
            messages.error(request, "Must be six character")
            return redirect('coupon')
        
        Coupons.objects.create(coupon_code=coupon_code, expiry_date=expiry_date, percentage=percentage)
        messages.success(request, "Coupon added successfully!")
        return redirect('coupon')
    
    return render(request, 'admin/coupons.html')

def sale(request):
    return render(request, 'admin/sale.html')