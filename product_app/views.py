from django.http import JsonResponse
from django.shortcuts import render,redirect
from . models import Product
from category_app.models import Paint, Art
from django.shortcuts import get_object_or_404
from django.contrib import messages



#=================== ADD PRODUCT ========================

from django.core.exceptions import ValidationError

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        paint_type = request.POST.get('paint_type')
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        # Backend validation to ensure files are images
        def validate_image(file):
            valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if file and file.content_type not in valid_mime_types:
                raise ValidationError('Only image files are allowed.')

        try:
            validate_image(image1)
            validate_image(image2)
            validate_image(image3)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('add_product')

        paint = Paint.objects.get(id=paint_type)
        art = Art.objects.get(id=category_name)
        Product.objects.create(
            product_name=product_name,
            description=description,
            paint_category=paint,
            art_category=art,
            images1=image1,
            images2=image2,
            images3=image3,
        )
        return redirect('product')

    return render(request, 'admin/product.html')



#================= PRODUCT STATUS =================#

def product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.product_status == True:
        product.product_status = False
    else:
        product.product_status = True
    product.save()
    return redirect('product')


#================== EDIT PRODUCT =================#


def edit_product(request, product_id):
    """Handle the product edit."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        art_type = request.POST.get('art_type')
        paint_type = request.POST.get('paint_type')

        product.art_category = get_object_or_404(Art, art_type=art_type)
        product.paint_category = get_object_or_404(Paint, paint_type=paint_type)
        product.save()

        return redirect('product_list')

    # Return product data as JSON for the modal
    data = {
        'product_name': product.product_name,
        'art_type': product.art_category.art_type,
        'paint_type': product.paint_category.paint_type,
    }
    return JsonResponse(data)