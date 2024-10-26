# from django.shortcuts import redirect, render
# from . models import Coupons
# from django.shortcuts import get_object_or_404
# from django.contrib import messages


# # Create your views here.
# def add_coupon(request):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect('admin_login')
    
    
#     if request.method == 'POST':
#         coupon_name = request.POST.get('coupon_name').strip()
#         low = coupon_name.lower()
#         all_coupons = [coupon.coupon_name.lower() for coupon in Coupons.objects.all()]

#         if low in all_coupons:
#             messages.error(request, "Coupon already exists.")
#             return redirect('coupons')
        
#         for existing_coupon in all_coupons:
#             if low in existing_coupon:
#                 messages.error(request, f"coupon '{coupon_name}' is too similar to '{existing_coupon}'.")
#                 return redirect('coupons')


#         if Coupons.objects.filter(coupon_code=coupon_name).exists():
#             messages.error(request, "Coupon already exists.")
#             return redirect('coupons')
        
#         if len(coupon_name) > 10:
#             messages.error(request, "Coupon code cannot exceed 10 characters.")
#             return redirect('coupons')
        
#         Coupons.objects.create(coupon_code=coupon_name)
#         messages.success(request, "Coupon added successfully!")
#         return redirect('coupons')
    
#     return render(request, 'admin/coupons.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Coupons
import random
import string

def generate_coupon_code(length=8):
    """Generate a random alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# def coupon_list(request):
#     """View to list all coupons."""
#     coupons = Coupons.objects.all()
#     return render(request, 'coupons/coupon_list.html', {'coupons': coupons})

def add_coupon(request):
    """View to add a new coupon."""
    if request.method == 'POST':
        percentage = request.POST.get('percentage')
        expiry_date = request.POST.get('expiry_date')
        coupon_code = generate_coupon_code()  # Generate coupon code

        try:
            Coupons.objects.create(
                coupon_code=coupon_code,
                percentage=percentage,
                expiry_date=expiry_date
            )
            messages.success(request, f'Coupon {coupon_code} added successfully!')
            return render(request, 'admin/art.html')
        
        except Exception as e:
            messages.error(request, f'Error adding coupon: {e}')
        return redirect('coupons')

def edit_coupon(request, pk):
    """View to edit an existing coupon."""
    coupon = get_object_or_404(Coupons, pk=pk)
    if request.method == 'POST':
        coupon.percentage = request.POST.get('percentage')
        coupon.expiry_date = request.POST.get('expiry_date')

        try:
            coupon.save()
            messages.success(request, f'Coupon {coupon.coupon_code} updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating coupon: {e}')
        return redirect('coupons')



