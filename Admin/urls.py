from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',views.login_admin, name='login_admin'),
    path('panel/',views.panel, name='panel'),
    path('productadd',views.productadd, name='productadd'),
    path('users/',views.users, name='users'),
    path('all_orders/',views.all_orders, name='all_orders'),
    path('order_items/<int:order_id>/',views.order_items, name='order_items'),
    path('art/',views.art, name='art'),
    path('coupon/',views.coupon, name='coupon'),
    path('paint/',views.paint, name='paint'),
    path('variant/<int:product_id>/',views.variant, name='variant'),
    path('product/',views.product, name='product'),
    path('user_status/<int:user_id>/',views.user_status, name='user_status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('remove_coupon/<int:coupon_id>', views.remove_coupon, name='remove_coupon'),
    
    
    
    

]

