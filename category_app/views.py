from django.shortcuts import render,redirect
from . models import Art,Paint
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re


#======================= ART ADDING SECTION ===================#

def add_art(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    if request.method == 'POST':
        art_type = request.POST.get('art_type').strip()
        low = art_type.lower()
        all_art_types = [art.art_type.lower() for art in Art.objects.all()]

        if low in all_art_types:
            messages.error(request, "Art type already exists.")
            return redirect('art')
        
        for existing_art in all_art_types:
            if low in existing_art:
                messages.error(request, f"Art type '{art_type}' is too similar to '{existing_art}'.")
                return redirect('art')

        if Art.objects.filter(art_type=art_type).exists():
            messages.error(request, "Art type already exists.")
            return redirect('art')
        
        if len(art_type) > 100:
            messages.error(request, "Art type cannot exceed 100 characters.")
            return redirect('art')
        
        if re.search(r'\d', art_type):
            messages.error(request, "Art type cannot contain numbers.")
            return redirect('art')
      
        Art.objects.create(art_type=art_type)
        messages.success(request, "Art type added successfully!")
        return redirect('art')
    
    return render(request, 'admin/art.html')


#======================= PAINT ADDING SECTION ==================#

def add_paint(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    if request.method == 'POST':
        paint_type = request.POST.get('add_paint').strip()
        low = paint_type.lower()
        all_paint_types = [paint.paint_type.lower() for paint in Paint.objects.all()]


        if low in all_paint_types:
            messages.error(request, "Paint type already exists.")
            return redirect('paint')
        
        for existing_paint in all_paint_types:
            if low in existing_paint:
                messages.error(request, f"Paint type '{paint_type}' is too similar to '{existing_paint}'.")
                return redirect('paint')

        if Paint.objects.filter(paint_type=paint_type).exists():
            messages.error(request, "Pain type already exists.")
            return redirect('paint')
        
        if len(paint_type) > 100:
            messages.error(request, "Paint type cannot exceed 100 characters.")
            return redirect('paint')
        
        if re.search(r'\d', paint_type):
            messages.error(request, "Paint type cannot contain numbers.")
            return redirect('paint')

        Paint.objects.create(paint_type = paint_type)
        return redirect ('paint')
    return render(request,'admin/paint.html')


#======================= ART AND PAINT STATUS =========================#

def art_status(request,art_id):
    art = get_object_or_404(Art,id = art_id)
    if art.art_type_status == True:
        art.art_type_status = False
    else:
        art.art_type_status = True
    art.save()
    return redirect('art')

def paint_status(request,paint_id):
    paint = get_object_or_404(Paint,id = paint_id)
    if paint.paint_type_status == True:
        paint.paint_type_status = False
    else:
        paint.paint_type_status = True
    paint.save()
    return redirect('paint')
 

#======================== ART AND PAINT EDITING SECTION ======================#

def edit_art(request):
    art_id = request.POST.get('categoryId')
    new_type = request.POST.get('art_type').strip()
    art = get_object_or_404(Art, id = art_id)

    if re.search(r'\d', new_type):
        messages.error(request, "Art type cannot contain numbers.")
        return redirect('art')
    
    if len(new_type) > 100:
        messages.error(request, "Art type cannot exceed 100 characters.")
        return redirect('art')
    
    art.art_type=new_type
    art.save()
    messages.success(request, "Success")
    return redirect('art')


def edit_paint(request):
    paint_id = request.POST.get('categoryId')
    new_type = request.POST.get('Paint_type').strip()
    paint = get_object_or_404(Paint, id = paint_id)
    
    if re.search(r'\d', new_type):
        messages.error(request, "Paint type cannot contain numbers.")
        return redirect('paint')
    
    if len(new_type) > 100:
        messages.error(request, "Paint type cannot exceed 100 characters.")
        return redirect('paint')
    
    paint.paint_type=new_type
    paint.save()
    messages.success(request, "Success")
    return redirect('paint')

