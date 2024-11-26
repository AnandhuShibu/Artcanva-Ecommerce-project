from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('User.urls')),
    path('a/',include('Admin.urls')),
    path('accounts/', include('allauth.urls')),
    path('product/',include('product_app.urls')),
    path('variant/',include('variant_app.urls')),
    path('category/',include('category_app.urls'))
    
   
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)