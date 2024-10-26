from django.urls import path
from . import views

urlpatterns = [
   
    path('add/', views.add_coupon, name='add_coupon'),
    path('edit/<int:pk>/', views.edit_coupon, name='edit_coupon'),
]


