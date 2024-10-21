from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from . models import Variant,Product

#================ VARIANT STATUS ================#


def variant_status(request, variant_id, product_id ):
    variant = get_object_or_404(Variant, id=variant_id)
    product = get_object_or_404(Product, id=product_id)
    if variant.variant_status == True:
        variant.variant_status = False
    else:
        variant.variant_status = True
    variant.save()
    return redirect('variant', product_id=product.id )