from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'variant_app'
urlpatterns = [
    path('variant_status/<int:variant_id>/<int:product_id>/',views.variant_status, name='variant_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)