from django.urls import path
from . import views
from .views import user_logout, submit_review

from .views import sales_report, export_sales_report
# from .views import place_order, razorpay_checkout

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('otp/',views.otp,name='otp'),
    path('login/',views.login, name='login'),
    path('',views.home, name='home'),
    path('resend_otp/',views.resend_otp, name='resend_otp'),
    path('shop',views.shop, name='shop'),
    path('jasir',views.jasir, name='jasir'),
    path('error',views.error, name='error'),
    path('email/',views.email_verify,name='email_varify'),
    path('resend/',views.resend_otp_password, name='resend'),
    path('passwordotp/',views.password_otp,name='password_otp'),
    path('newpassword',views.new_password,name='new_password'),
    path('cart/',views.cart,name='cart'),
    path('addcart/<int:product_id>/<int:variant_id>/',views.add_cart,name='addcart'),
    path('add_wishlist_single/<int:product_id>/<int:variant_id>/',views.add_wishlist_single,name='add_wishlist_single'),

    
    path('profile',views.profile,name='profile'),
    path('single/<int:product_id>/<int:variant_id>/',views.single, name='single'),
    path('remove_cart_item/<int:variant_id>',views.remove_cart_item, name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout_og/',views.checkout_og,name='checkout_og'),
    path('user_logout/',views.user_logout, name='user_logout'),
    path('orders',views.orders, name='orders'),
    path('order_details/<int:order_id>',views.order_details, name='order_details'),
    path('order_placed',views.order_placed, name='order_placed'),
    path('user/logout/', user_logout, name='user_logout'),
    path('password_verify',views.password_verify, name='password_verify'),
    path('password_change',views.password_change, name='password_change'),
    path('edit_address/',views.edit_address, name='edit_address'),
    path('edit_address_chechout/',views.edit_address_chechout, name='edit_address_chechout'),
    path('remove_address/<int:address_id>',views.remove_address, name='remove_address'),
    path('remove_address_profile/<int:address_id>',views.remove_address_profile, name='remove_address_profile'),
    path('place_order/',views.place_order, name='place_order'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('add_wishlist/<int:product_id>/<int:variant_id>',views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist_item/<int:variant_id>', views.remove_wishlist_item, name='remove_wishlist_item'),
    path('add_cart_wishlist/<int:product_id>/<int:variant_id>',views.add_cart_wishlist, name='add_cart_wishlist'),

    
    path('place-order/', views.place_order, name='place_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('order_cancel/<int:order_id>', views.order_cancel, name= 'order_cancel'),
    # path('single_order_cancel/<int:order_id>/<int:product_id>/<int:variant_id>', views.single_order_cancel, name= 'single_order_cancel'),

    path('sales-report/', sales_report, name='sales_report'),
    path('export-sales-report/', export_sales_report, name='export_sales_report'),
    path('submit-review/<int:order_id>/<int:product_id>/<int:variant_id>', submit_review, name='submit_review'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    ]
