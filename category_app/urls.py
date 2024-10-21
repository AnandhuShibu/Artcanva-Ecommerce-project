from django.urls import path
from . import views


urlpatterns = [
    path('add_art/',views.add_art, name='add_art'),
    path('add_paint/',views.add_paint, name='add_paint'),
    path('art_status/<int:art_id>/',views.art_status, name= 'art_status'),
    path('paint_status/<int:paint_id>/',views.paint_status, name= 'paint_status'),
    path('edit_art/', views.edit_art, name='edit_art'),
    path('edit_paint/', views.edit_paint, name='edit_paint'),

]