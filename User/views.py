import random
import re
import string
import time
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login as authlogin,logout as authlogout,update_session_auth_hash
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
import razorpay


from product_app.models import Product
from variant_app.models import Variant
from category_app.models import Paint, Art
from django.shortcuts import get_object_or_404
# from django.db.models import OuterRef, Subquery
from User.models import Address,Cart
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . models import Order,Order_details, Review, Wishlist
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

from django.db import transaction

# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


#============= USER SIGNUP ============#

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()

        if User.objects.filter(Q(username = username)).exists():
            messages.info(request,'USER NAME ALREADY TAKEN')
            return redirect('signup')
        if len(username) < 5:
            messages.info(request, 'Username must be at least 5 characters long.')
            return redirect('signup')
        
        if len(password1) < 8:
            messages.info(request, 'Password must be at least 8 characters long')
            return redirect('signup')
        
        if password1 != password2:
            messages.info(request, 'PASSWORD DO NOT MATCH !')
            return redirect('signup')
        else:
            user = User.objects.create_user(username = username, email = email, password = password1)
            generated_otp = create_otp()
            send_otp_email(email, generated_otp)
            store_otp_in_session(request, generated_otp)
            request.session['email'] = email
            return redirect('otp')
        
    return render(request, 'user/signup.html')


#============= USER OTP SECTION =============#

def create_otp(length=4):
    digits = string.digits
    generated_otp = ''.join(random.choice(digits) for _ in range(length))
    return generated_otp

def send_otp_email(user_email, generated_otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {generated_otp}. It is valid for 1 minute.'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

def store_otp_in_session(request, generated_otp):
    expiry_time = time.time() + 60  # OTP valid for 1 minute
    request.session['generated_otp'] = generated_otp
    request.session['otp_expiry'] = expiry_time

def is_otp_valid(request, input_otp):
    stored_otp = request.session.get('generated_otp')
    expiry_time = request.session.get('otp_expiry')

    if not stored_otp or not expiry_time:
        return False
    if time.time() < expiry_time and stored_otp == input_otp:
        return True
    return False

def otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('input_otp')
        print(input_otp)
        if is_otp_valid(request, input_otp):
            del request.session['generated_otp']
            del request.session['otp_expiry']
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp')

    otp_expiry = request.session.get('otp_expiry', 0)
    remaining_time = int(otp_expiry - time.time())
    remaining_time = max(remaining_time, 0)

    return render(request, 'user/otp.html', {
        'remaining_time': remaining_time
    })


#============== USER LOGIN ===============#

@never_cache 
def login(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user:
            authlogin(request,user)
            return redirect('home')
        else:
            messages.info(request,'INVALID USERNAME OR PASSWORD')
            return redirect('login')
    return render(request,'user/login.html')


def resend_otp(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, 'Email not found in session. Please start the signup process again.')
        return redirect('signup')

    otp = create_otp()
    send_otp_email(email, otp)
    store_otp_in_session(request, otp)
    messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('otp')

#=============== USER LOGOUT ==============#

def user_logout(request):
    logout(request)
    return redirect('home')


#=============== RESET PASSWORD ==================#

def email_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp = create_otp()
            send_otp_email(email, otp)
            store_otp_in_session(request, otp)
            request.session['email'] = email
            return redirect('password_otp')
        else:
            messages.error(request, 'Email address not found.')
            return redirect('email_varify')
    return render(request,'user/emailvarify.html')

def password_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        if not input_otp:
            messages.error(request, 'Please enter the OTP.')
            return redirect('password_otp.html')
        if is_otp_valid(request, input_otp):
            messages.success(request, 'OTP verified successfully!')
            return redirect('new_password')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            redirect('password_otp')

    otp_expiration = request.session.get('otp_expiration', 0)
    remaining_time = int(otp_expiration - time.time())
    remaining_time = max(remaining_time, 0)

    return render(request, 'user/password_otp.html',{'remaining_time': remaining_time})

def resend_otp_password(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'Email not found in session. Please start the signup process again.')
        return redirect('email_varify')
    otp = create_otp()
    send_otp_email(email, otp)
    store_otp_in_session(request, otp)
    messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('password_otp')


def new_password(request):
    email = request.session.get('email')
    if request.method == 'POST':
        newpassword = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        if len(newpassword) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif newpassword != confirm_password:
            messages.error(request, 'The new password and confirm password do not match.')
        else:
            try:
                user = User.objects.get(email = email)
                user.set_password(newpassword)
                user.save()
                messages.success(request, 'Password changed successfully. Please log in with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with the provided email address.')

    return render(request,'user/newpassword.html')


#================= HOME SECTION =====================#

def home(request):
    arrivals = Product.objects.filter(product_status = True).order_by('-id')[:3]
    populars = Product.objects.filter(product_status = True)[:4]
    context = {
        'arrivals': arrivals,
        'populars': populars
    }
    return render(request,'user/home.html', context)


#================= SHOP SECTION ===============#

def shop(request):
    search_query = request.GET.get('q', '').strip()  # Get search query, default to an empty string

    # Default empty selections
    selected_categories = request.POST.getlist('categories') if request.method == 'POST' else []
    selected_size = request.POST.getlist('size') if request.method == 'POST' else []
    price_order = request.POST.get('price_order') if request.method == 'POST' else None

    # Fetch all products initially
    products = Product.objects.all()

    # Apply filters based on user selection
    if selected_categories:
        products = products.filter(art_category__id__in=selected_categories)

    if selected_size:
        products = products.filter(variants__id__in=selected_size)

    if price_order:
        if price_order == 'asc':
            products = products.order_by('variants__price')
        elif price_order == 'desc':
            products = products.order_by('-variants__price')

    # Apply search filter if a search query is provided
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Pagination: always apply pagination regardless of request method
    paginator = Paginator(products, 9)  # Show 10 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the corresponding page

    # Check if no products are found
    no_products_found = not products.exists()

    # Fetch additional data
    unique_frame_sizes = Variant.objects.order_by('frame_size').distinct()
    paints = Paint.objects.all()
    arts = Art.objects.all()

    # Prepare context for template rendering
    context = {
        'products': page_obj.object_list,  # Use paginated products for display
        'paints': paints,
        'arts': arts,
        'variants': unique_frame_sizes,
        'selected_categories': selected_categories,
        'selected_size': selected_size,
        'no_products_found': no_products_found,
        'search_query': search_query,
        'page_obj': page_obj,  # Pass the page object to the template
    }

    # Render the template with context
    return render(request, 'user/shop.html', context)


#================= SINGLE PRODUCT SECTION ===============#

from django.shortcuts import render, get_object_or_404
from .models import Product, Variant, Cart

def single(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(Variant, id=variant_id)
    sizes = Variant.objects.filter(product=product)

    in_cart = None

    if request.user.is_authenticated:
        in_cart = Cart.objects.filter(user=request.user, variant=variant).exists()

    return render(request, 'user/single.html', {
        'product': product,
        'variant': variant,
        'sizes': sizes,
        'in_cart': in_cart,  # Pass the flag to the template
    })

def jasir(request):
    return render(request, 'user/jasir.html')

def change(request):
    return render(request, 'user/password_verify.html')


#================= USER PROFILE SECTION =================#

def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "PLEASE LOGIN.")
        return redirect('login')
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')

        errors = []

        if not fullname or len(fullname) < 3 or not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must be at least 3 characters long.")

        if not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must contain only alphabets")

        pattern = r"^[6-9]\d{9}$"

        if not re.match(pattern, mobile):
            errors.append("Please Enter Valid Phone Number")

        if not pincode.isdigit() or len(pincode) != 6:
            errors.append("Pincode must be a 6-digit number.")

        if not address or len(address) < 5:
            errors.append("Address must be at least 5 characters long.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('profile')
        
        Address.objects.create(
            fullname=fullname,
            mobile=mobile,
            pincode=pincode,
            address=address,
            city=city,
            district=district,
            state=state,
            user_id=request.user
            )
        return redirect('profile')
        
    informations = Address.objects.filter(user_id_id = request.user)
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        password = request.user.password
    print(password)
    context = {
        'informations':informations,
        'username': username,
        'email': email
    }
    return render(request,'user/profile.html', context)


def edit_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')

        if address_id:
            address_instance = get_object_or_404(Address, id=address_id)
            address_instance.fullname = fullname
            address_instance.mobile = mobile
            address_instance.pincode = pincode
            address_instance.address = address
            address_instance.city = city
            address_instance.district = district
            address_instance.state = state
            address_instance.save()
        else:
            Address.objects.create(
                fullname=fullname, mobile=mobile, pincode=pincode,
                address=address, city=city, district=district, state=state, user_id=request.user
            )
        return redirect('profile')

def remove_address_profile(request,address_id):
    address = Address.objects.filter(id=address_id)
    address.delete()    
    return redirect('profile')


#============== CHANGE PASSWORD SECTION =============#

def password_verify(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        if check_password(old_password, request.user.password):
            return redirect('password_change')
        else:
            messages.error(request, '')
            return redirect('password_verify')
    
    return render(request, 'user/password_verify.html')


def password_change(request):
    if request.method == "POST":
        newpassword = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirm_password')

        if newpassword == confirm_password:
            user = request.user
            user.set_password(newpassword)
            user.save()
            update_session_auth_hash(request,request.user)
            return redirect('profile')

    return render(request, 'user/password_change.html')


#=================== CART SECTION ===================#

def cart(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in view Cart.")
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user).order_by('-id')
    is_empty = not cart_items.exists()

    


    return render(request,'user/cart.html', {'cart_items': cart_items, 'is_empty': is_empty})


def add_cart(request,product_id, variant_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to add items to your cart.")
        return redirect('login')
    
    product_id = get_object_or_404(Product, id=product_id)
    variant_id = get_object_or_404(Variant,id = variant_id)
    cart_item_exists = Cart.objects.filter(variant=variant_id, user=request.user).exists()
    if cart_item_exists:
        messages.warning(request, "This item is already in your cart.")
        return redirect('single', product_id=product_id.id, variant_id=variant_id.id)
    Cart.objects.create(product=product_id, user=request.user, variant=variant_id)
    return redirect('cart')

def remove_cart_item(request, variant_id):
    cart_items = Cart.objects.get(variant=variant_id, user=request.user)
    cart_items.delete()    
    return redirect('cart')


#====================== CHECK OUT SECTION ===================#

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, Variant

def checkout_og(request):
    if request.method == 'POST':
        total_price = request.POST.get('total_price')
        quantities = {
            key.split('_')[1]: int(value)
            for key, value in request.POST.items()
            if key.startswith('quantity_')
        }

        for variant_id, quantity in quantities.items():
            variant = get_object_or_404(Variant, id=variant_id)

            if quantity < 1:
                messages.error(request, "Quantity cannot be less than 1.")
                return redirect('cart')
            
            # elif quantity > 10:  # Check for maximum purchase limit
            #     messages.error(request, "Purchase quantity cannot exceed 10.")
            #     return redirect('cart')
            
            if quantity > variant.stock:
                messages.error(request, f"Only {variant.stock} items available for {variant.product.product_name}.")
                return redirect('cart')

            cart_item = get_object_or_404(Cart, user=request.user, variant_id=variant_id)
            cart_item.quantity = quantity
            cart_item.save()

        request.session['total_price'] = total_price
        return redirect('checkout')
    return redirect('cart')


def checkout(request):
    if not request.user.is_authenticated:
        messages.info(request, "PLEASE LOGIN.")
        return redirect('login')
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')

        errors = []

        if not fullname or len(fullname) < 3 or not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must be at least 3 characters long.")

        if not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must contain only alphabets")

        pattern = r"^[6-9]\d{9}$"

        if not re.match(pattern, mobile):
            errors.append("Please Enter Valid Phone Number")

        if not pincode.isdigit() or len(pincode) != 6:
            errors.append("Pincode must be a 6-digit number.")

        if not address or len(address) < 5:
            errors.append("Address must be at least 5 characters long.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('checkout')

        Address.objects.create(
            fullname=fullname,
            mobile=mobile,
            pincode=pincode,
            address=address,
            city=city,
            district=district,
            state=state,
            user_id=request.user
            )
        return redirect('checkout')
    
    all_address = Address.objects.filter(user_id_id = request.user)
    total_price = request.session.get('total_price', 0)
    cart_items=Cart.objects.filter(user=request.user)

    
    return render(request,'user/checkout.html', {'all_address': all_address, 'total_price':total_price, 'cart_items':cart_items})

def edit_address_chechout(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')

        errors = []

        if not fullname or len(fullname) < 3 or not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must be at least 3 characters long.")

        if not fullname.replace(" ", "").isalpha():
            errors.append("Fullname must contain only alphabets")

        pattern = r"^[6-9]\d{9}$"

        if not re.match(pattern, mobile):
            errors.append("Please Enter Valid Phone Number")

        if not pincode.isdigit() or len(pincode) != 6:
            errors.append("Pincode must be a 6-digit number.")

        if not address or len(address) < 5:
            errors.append("Address must be at least 5 characters long.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('checkout')

        if address_id:
            address_instance = get_object_or_404(Address, id=address_id)
            address_instance.fullname = fullname
            address_instance.mobile = mobile
            address_instance.pincode = pincode
            address_instance.address = address
            address_instance.city = city
            address_instance.district = district
            address_instance.state = state
            address_instance.save()
        else:
            Address.objects.create(
                fullname=fullname, mobile=mobile, pincode=pincode,
                address=address, city=city, district=district, state=state, user_id=request.user
            )
        return redirect('checkout')

def remove_address(request,address_id):
    address = Address.objects.filter(id=address_id)
    address.delete()    
    return redirect('checkout')


#================== PLACE ORDER SECTION ==================#

def place_order(request):
    cart_items=Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        selected_address_id = request.POST.get('selected_address')
        selected_address = Address.objects.get(id=selected_address_id)
        ordered_items = Cart.objects.all()
        total_price = int(request.session.get('total_price', 0)) * 100
        print(ordered_items)
        
 
        order=Order.objects.create(
            user=request.user,
            total_amount=total_price,
            payment_method=payment_method,
            address=selected_address
        )
        for item in cart_items:
            Order_details.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                variant=item.variant
            )
            item.variant.stock -= item.quantity
            item.variant.save()
        
        cart_items=Cart.objects.filter(user=request.user)
        cart_items.delete()
       
        return redirect('order_placed')
            

#============================ SAMPLE ===============================


# from django.views.decorators.csrf import csrf_exempt

# # Initialize Razorpay client
# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# def place_order(request):
#     print('firsttttttttttttttttt')
#     cart_items = Cart.objects.filter(user=request.user)
    
#     if request.method == 'POST':
#         payment_method = request.POST.get('payment_method')
#         selected_address_id = request.POST.get('selected_address')
#         selected_address = Address.objects.get(id=selected_address_id)
#         total_price = int(request.session.get('total_price', 0)) * 100  # Amount in paisa
        
#         # Check if the payment method is COD or Razorpay
#         if payment_method == 'COD':
#             # Handle Cash on Delivery
#             order = Order.objects.create(
#                 user=request.user,
#                 total_amount=total_price,
#                 payment_method=payment_method,
#                 address=selected_address,
#                 payment_status='Pending'  # Mark as unpaid initially
#             )

#             for item in cart_items:
#                 Order_details.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     variant=item.variant
#                 )
#                 item.variant.stock -= item.quantity
#                 item.variant.save()

#             # Clear the cart after creating the order
#             cart_items.delete()

#             # Redirect to order placed confirmation page
#             return redirect('order_placed')

#         elif payment_method == 'Razorpay':
#             # Handle Razorpay payment
#             razorpay_order = client.order.create({
#                 'amount': total_price,
#                 'currency': 'INR',
#                 'payment_capture': '1'
#             })
#             print('aaaaaaaaaaaaaaaaa')

#             order = Order.objects.create(
#                 user=request.user,
#                 total_amount=total_price,
#                 payment_method=payment_method,
#                 address=selected_address,
#                 payment_status='Paid'  # Save Razorpay order ID
#             )

#             for item in cart_items:
#                 Order_details.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     variant=item.variant
#                 )
#                 item.variant.stock -= item.quantity
#                 item.variant.save()

#             # Clear the cart after creating the order
#             cart_items.delete()

#             # Redirect to Razorpay payment page
#             return render(request, 'user/payment.html', {
#                 'order': order,
#                 'razorpay_order_id': razorpay_order['id'],
#                 'razorpay_key': settings.RAZORPAY_KEY_ID,
#                 'amount': total_price
#             })
#         return redirect('order_placed')
           

# @csrf_exempt
# def payment_verification(request):
    
#     print('bbbbbbbbbbbbbbbbbb')
#     if request.method == 'POST':
#         data = request.POST
#         razorpay_order_id = data.get('razorpay_order_id')
#         razorpay_payment_id = data.get('razorpay_payment_id')
#         razorpay_signature = data.get('razorpay_signature')

#         try:
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_signature': razorpay_signature
#             })
            
#             # Mark order as paid after successful verification
#             order = Order.objects.filter(user=request.user, total_amount=data['amount']).last()  # Adjust logic as necessary
#             if order:
#                 order.payment_status = 'Paid'  # Update payment status
#                 order.save()
#             return redirect('order_placed')
        
#         except razorpay.errors.SignatureVerificationError:
#             # Redirect to payment failure page if verification fails
#             return redirect('payment_failed')

#     return redirect('home')


# def order_placed(request):
#     return render(request, 'order_placed.html')

# def payment_failed(request):
#     print('ccccccccccccccccccccc')
#     return render(request, 'payment_failed.html')


#==================== ORDERS SECTION ==================#

def orders(request):
    orders=Order.objects.filter(user=request.user)
    no_user_orders_found = not orders.exists()
    return render(request, 'user/orders.html', {'orders':orders, 'no_user_orders_found': no_user_orders_found})

def order_details(request, order_id):
    orders = get_object_or_404(Order, id=order_id)
    order_items=Order_details.objects.filter(order = orders)
    return render(request, 'user/order_details.html', {'order_items':order_items, 'orders':orders})

def order_placed(request):
    return render(request, 'user/order_placed.html')


#================ RATINGS AND REVIEWS ==========#





# @csrf_exempt  # For simplicity, but consider using CSRF tokens in production
def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        # Save the review to your database
        Review.objects.create(product_id=product_id, rating=rating, review=review)

        return JsonResponse({'message': 'Review submitted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


#==================== WISHLIST SECTION ================#

# def wishlist(request):
#     return render(request,'user/wishlist.html')


def wishlist(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in view wishlist.")
        return redirect('login')
    
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-id')

    paginator = Paginator(wishlist_items, 3)  # Show 10 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the corresponding page

   
    is_empty = not wishlist_items.exists()
    return render(request,'user/wishlist.html', {'is_empty': is_empty, 'page_obj': page_obj})


def add_wishlist(request,product_id, variant_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to add items to your wishlist.")
        return redirect('login')
    
    product_id = get_object_or_404(Product, id=product_id)
    variant_id = get_object_or_404(Variant,id = variant_id)
    wishlist_item_exists = Wishlist.objects.filter(user=request.user, variant=variant_id).exists()
    if wishlist_item_exists:
        messages.warning(request, "This item is already in your wishlist.")
        return redirect('shop')
    Wishlist.objects.create(product=product_id, user=request.user, variant=variant_id)
    return redirect('wishlist')

def remove_wishlist_item(request, variant_id):
    print("hhhgh")
    wishlist_items = Wishlist.objects.get(variant=variant_id, user=request.user)
    wishlist_items.delete()    
    return redirect('wishlist')


