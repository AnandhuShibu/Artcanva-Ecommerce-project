import re
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
from User.models import Order,Order_details,Address,Return,Wallet,Wallet_Transaction,OrderAddress
from datetime import datetime, timedelta
from django.db.models import Sum,F
from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from django.http import HttpResponse
from coupon_app . models import Coupon_user, Coupons
from django.utils import timezone
from django.db.models.functions import Round




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
    search_query = request.GET.get('q', '').strip() 

    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    paint = Paint.objects.all()
    art = Art.objects.all()
    products = Product.objects.all().order_by('-id')
    
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    
    paginator = Paginator(products, 7) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    no_products_found = not products.exists()

    context = {
        'paint':paint,
        'art':art,
        'page_obj': page_obj,
        'search_query': search_query,
        'no_products_found': no_products_found,
    }
    return render(request,'admin/product.html', context)


#------------------------- EDIT PRODUCT SECTION ----------------------#

def edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        art_category_id = request.POST.get('art_category')
        paint_category_id = request.POST.get('paint_category')
        
        
        if not art_category_id or not paint_category_id:
            print("not")
            messages.error(request, "Please select both Art Category and Paint Category.")
            return redirect('product') 

        if Product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
            messages.error(request, "Product name already exists")
            return redirect('product')
        
        if not re.match(r'^[a-zA-Z0-9\s]+$', product_name):
            messages.error(request, "Product name should not contain special characters.")
            return redirect('product')
        
        product = get_object_or_404(Product, id=product_id)
        product.product_name = product_name
        product.art_category_id = art_category_id
        product.paint_category_id = paint_category_id
        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('product')
 
    
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


#----------------------- VARIANTS SECTION --------------------------#

def variant(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('login_admin')
    
    products = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(product=products).order_by('-id')

    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        size = request.POST.get('size')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if variant_id:
            variant = get_object_or_404(Variant, id=variant_id)
            variant.frame_size = size
            variant.price = price
            variant.stock = stock
            variant.save()
        else: 
            existing_variant = Variant.objects.filter(product=products, frame_size=size).first()
            if existing_variant:
                return render(request, 'admin/variant.html', {
                    'page_obj': variants,
                    'error_message': "!"
                })
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


#---------------------- ORDERS SECTION -------------------#

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
    order_address = get_object_or_404(OrderAddress, order=order_id)

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

        if new_status == 'Delivered':
            order.deliver_date = timezone.now()
        else:
            order.deliver_date = None
        order.save()
        return redirect('order_items', order_id=order_id)


#-------------------- COUPONS SECTION ---------------------#

def coupon(request):
    search_query = request.GET.get('q', '').strip()
    coupons = Coupons.objects.all()
    if search_query:
        coupons = coupons.filter(coupon_code__icontains=search_query)
       
    paginator = Paginator(coupons, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    no_coupon_found = not coupons.exists()

    return render(request,'admin/coupons.html', {'page_obj': page_obj, 'no_coupon_found': no_coupon_found})

def remove_coupon(request, coupon_id):
    coupon_item = Coupons.objects.get(id = coupon_id)
    coupon_item.delete()    
    return redirect('coupon')

def edit_coupon(request):
    coupon_id = request.POST.get('categoryId')
    edit_coupon = request.POST.get('edit_coupon').strip()
    percentage = request.POST.get('percentage').strip()
    expiry_date = request.POST.get('expiry_date').strip()
    coupon = get_object_or_404(Coupons, id = coupon_id)
    
    if len(edit_coupon) > 6:
        messages.error(request, "Paint type cannot exceed 6 characters.")
        return redirect('coupon')
    
    Coupons.coupon_code=edit_coupon
    Coupons.save()
    messages.success(request, "Success")
    return redirect('coupon')

def add_coupon(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code').strip().upper()
        percentage = request.POST.get('percentage').strip()
        expiry_date = request.POST.get('expiry_date').strip()

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



#-------------------------- OFFER SECTION ------------------------#

def offer(request):

    offers = Art.objects.filter(art_type_offer__gt=0)

    return render(request, 'admin/offer.html', {'offers': offers})

def add_offer_page(request):
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('login_admin')
    art = Art.objects.filter(art_type_status=True)
    context = {
        'arts': art
    }
    return render(request, 'admin/add_offer.html', context)


def add_offer(request):
    if request.method == 'POST':
        category_name_id = request.POST.get('category_name')
        offer_percentage = request.POST.get('percentage')
        if offer_percentage and category_name_id:
            try:
                offer_percentage = int(offer_percentage)

                try:
                    art_instance = Art.objects.get(id=category_name_id) 
                    art_instance.art_type_offer = offer_percentage 
                    art_instance.save() 
                except Art.DoesNotExist:
                    print("Art instance not found for ID:", category_name_id)

            except ValueError:
                print("Invalid percentage value.")
        return redirect('offer')
    return render(request, 'admin/offer.html')


def remove_offer(request, offer_id):
    offer = get_object_or_404(Art, id=offer_id)
    offer.art_type_offer = 0  # Set the offer percentage to 0%
    offer.save()
    return redirect('offer')


#----------------------- SALES SECTION -------------------------#


def sale(request):
    return render(request, 'admin/sale.html')




from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.core.paginator import Paginator

from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.core.paginator import Paginator

from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.core.paginator import Paginator

def sales(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_type = request.GET.get('status')
    orders = Order.objects.filter(status='Delivered').order_by('-id')

    # Debugging prints to check the date filtering logic
    print("start_date", start_date)
    print("end_date", end_date)
    print("filter_type", filter_type)

    # Handle different filter types (daily, weekly, monthly)
    if filter_type == 'daily':
        print("Daily filter applied")
        today = datetime.now().date()
        start_date = today
        end_date = today

    elif filter_type == 'weekly':
        print("Weekly filter applied")
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
        end_date = today + timedelta(days=(6 - today.weekday()))  # End of the week (Sunday)

    elif filter_type == 'monthly':
        print("Monthly filter applied")
        today = datetime.now().date()
        start_date = today.replace(day=1)  # First day of the month
        end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of the month

    # Ensure the start_date and end_date are in date format
    if start_date and isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date and isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Debugging prints to check if dates are parsed correctly
    print("Parsed start_date:", start_date)
    print("Parsed end_date:", end_date)

    # Apply date filtering only if both dates are valid
    if start_date and end_date:
        print("Filtering orders by date range")
        orders = orders.filter(order_date__date__range=(start_date, end_date))  # Use order_date__date to strip time part

    # Pagination logic
    paginator = Paginator(orders, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate overall sales count, total amount, and overall discount
    overall_sales_count = orders.count()
    overall_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    overall_discount = (
        orders.filter(coupon__isnull=False)
        .annotate(discount_amount=Round(F('total_amount') * F('coupon__percentage') / 100, 2))
        .aggregate(total_discount=Sum('discount_amount'))['total_discount'] or 0
    )

    context = {
        'page_obj': page_obj,
        'overall_sales_count': overall_sales_count,
        'overall_amount': overall_amount,
        'overall_discount': overall_discount,
    }

    return render(request, 'admin/sales.html', context)



from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Sum, F
from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore

def export_pdf(request):
    # Get filter parameters from the request
    filter_type = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Prepare the response and PDF document
    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    
    # Prepare the document
    doc = SimpleDocTemplate(response, pagesize=A4)
    doc.title = "ARTCANVA SALES REPORT"
    elements = []
    

    # Add the Heading
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.fontSize = 18  # Adjust font size
    heading_style.alignment = 1  # Center alignment
    
    heading = Paragraph("ARTCANVA SALES REPORT", heading_style)
    elements.append(heading)

    # Add some space after the heading
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Handle different filter types (daily, weekly, monthly)
    orders = Order.objects.filter(status='Delivered').order_by('-id')

    if filter_type == 'daily':
        today = datetime.now().date()
        start_date = today
        end_date = today

    elif filter_type == 'weekly':
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
        end_date = today + timedelta(days=(6 - today.weekday()))  # End of the week (Sunday)

    elif filter_type == 'monthly':
        today = datetime.now().date()
        start_date = today.replace(day=1)  # First day of the month
        end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of the month

    # Ensure start_date and end_date are valid date objects
    if start_date and isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date and isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Apply date filtering if both dates are valid
    if start_date and end_date:
        orders = orders.filter(order_date__date__range=(start_date, end_date))  # Filter by date range

     # Calculate total sales count, total amount, and total discount
    overall_sales_count = orders.count()
    overall_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Calculate discount amount (if coupon applied)
    overall_discount = (
        orders.filter(coupon__isnull=False)
        .annotate(discount_amount=Round(F('total_amount') * F('coupon__percentage') / 100, 2))
        .aggregate(total_discount=Sum('discount_amount'))['total_discount'] or 0
    )

    # Add summary information to the PDF
    summary_data = [
        f"Total Sales: {overall_sales_count}",
        f"Total Amount: {overall_amount}",
        f"Total Discount: {overall_discount}",
    ]
    for summary in summary_data:
        elements.append(Paragraph(summary, styles['Normal']))
    
    # Add some space after the summary
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Define the table data
    data = [
        ["Order ID", "Customer Name", "Total Amount", "Ordered at", "Delivered at", "Payment Method"]  # Header row
    ]

    # Add data for each order in the filtered set
    for order in orders:
        row = [
            str(order.id),
            order.user.username,
            f"{order.total_amount}",
            order.order_date.strftime('%Y-%m-%d'),
            order.deliver_date.strftime('%Y-%m-%d') if order.deliver_date else "Pending",
            order.payment_method
        ]
        data.append(row)

    # Create the table
    table = Table(data)
    
    # Style the table (alignment, border width, etc.)
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all columns to the center
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Grid lines for all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header row
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for table
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header background color
    ]))
    
    # Add the table to the document
    elements.append(table)

    # Build the PDF
    doc.build(elements)
    
    return response



#----------------------  CHANGING RETURN STATUS --------------------#

def return_request(request):
    return_items = Return.objects.all().order_by('-id')

    paginator = Paginator(return_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/return_request.html', {'page_obj': page_obj})


def return_status(request):
    if request.method == 'POST':
        return_id = request.POST.get('return_id')  # ID of the return request
        selected_status = request.POST.get('accept')  # Fetch the selected status
        
        if return_id and selected_status:
            return_item = get_object_or_404(Return, id=return_id)
            if selected_status == 'accepted':
                order_detail = get_object_or_404(Order_details, product=return_item.product, order__user=return_item.user)
                amount_to_refund = order_detail.variant.price * order_detail.quantity 
                
                # Add amount to user's wallet
                wallet, created = Wallet.objects.get_or_create(user=order_detail.order.user)
                wallet.wallet_amount += amount_to_refund
                wallet.save()

            return_item.status = selected_status
            return_item.save()

            print('HELLO')
            return redirect('return_request')
        
    return_items = Return.objects.filter(status='request').order_by('-id')
    return render(request, 'admin/return_request.html', {'return_items': return_items})

