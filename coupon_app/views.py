# from django.shortcuts import redirect, render
# from . models import Coupons
# from django.shortcuts import get_object_or_404
# from django.contrib import messages


# # Create your views here.
# def add_coupon(request):
#     print('hai jaseeeeeeeeeeeeer')
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect('admin_login')
    
#     if request.method == 'POST':
#         coupon_code = request.POST.get('coupon_code').strip().upper()
        
#         all_coupons = [coupon.coupon_code for coupon in Coupons.objects.all()]

#         if coupon_code in all_coupons:
#             messages.error(request, "Coupon already exists.")
#             return redirect('coupon')
        
#         for existing_coupon in all_coupons:
#             if coupon_code in existing_coupon:
#                 messages.error(request, f"coupon '{coupon_code}' is too similar to '{existing_coupon}'.")
#                 return redirect('coupon')


#         if Coupons.objects.filter(coupon_code=coupon_code).exists():
#             messages.error(request, "Coupon already exists.")
#             return redirect('coupon')
        
#         if len(coupon_code) < 6:
#             messages.error(request, "Must be six character")
#             return redirect('coupon')
        
#         Coupons.objects.create(coupon_code=coupon_code)
#         messages.success(request, "Coupon added successfully!")
#         return redirect('coupon')
    
#     return render(request, 'admin/coupons.html')


