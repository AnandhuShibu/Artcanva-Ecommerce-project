from django.shortcuts import render,redirect
from . models import Product
from category_app.models import Paint, Art
from django.shortcuts import get_object_or_404



#=================== ADD PRODUCT ========================

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        paint_type = request.POST.get('paint_type')
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        paint = Paint.objects.get(id = paint_type)
        art = Art.objects.get(id = category_name)
        Product.objects.create(
            product_name = product_name,
            description = description,
            paint_category = paint,
            art_category = art,
            images1 = image1,
            images2 = image2,
            images3 = image3,
        )
        return redirect('product')
    
    return render(request,'admin/product.html')


#================= PRODUCT STATUS =================#

def product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.product_status == True:
        product.product_status = False
    else:
        product.product_status = True
    product.save()
    return redirect('product')


