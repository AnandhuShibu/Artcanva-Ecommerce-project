from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',views.login_admin, name='login_admin'),
    path('panel/',views.panel, name='panel'),
    path('productadd',views.productadd, name='productadd'),
    path('users/',views.users, name='users'),
    # path('orders/',views.orders, name='orders'),
    path('art/',views.art, name='art'),
    path('paint/',views.paint, name='paint'),
    path('variant/<int:product_id>/',views.variant, name='variant'),
    path('product/',views.product, name='product'),
    path('user_status/<int:user_id>/',views.user_status, name='user_status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    

]

