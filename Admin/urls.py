from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('sales/',views.sales, name='sales'),
    path('offer/',views.offer, name='offer'),
    path('add_offer/',views.add_offer, name='add_offer'),
    path('add_offer_page/', views.add_offer_page, name='add_offer_page'), 
    path('paint/',views.paint, name='paint'),
    path('variant/<int:product_id>/',views.variant, name='variant'),
    path('product/',views.product, name='product'),
    path('user_status/<int:user_id>/',views.user_status, name='user_status'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('remove_coupon/<int:coupon_id>', views.remove_coupon, name='remove_coupon'),
    path('remove_offer/<int:offer_id>', views.remove_offer, name='remove_offer'),
    path('sales_report/export_pdf/', views.export_pdf, name='export_pdf'),
    path('return_request/',views.return_request, name='return_request'),
    path('return_status/',views.return_status, name='return_status'),
    path('edit_product/', views.edit_product, name='edit_product'),
    # path('saleschart/', views.sales_chart, name='sales_chart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sample/', views.sample, name='sample'),
    path('get_sales_data/', views.get_sales_data, name='get_sales_data'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

