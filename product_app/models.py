from django.db import models
from category_app.models import Paint, Art  

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    paint_category = models.ForeignKey(Paint, on_delete=models.CASCADE)
    art_category = models.ForeignKey(Art, on_delete=models.CASCADE)
    images1 = models.ImageField(upload_to='images/', blank=True, null=True)
    images2 = models.ImageField(upload_to='images/', blank=True, null=True)
    images3 = models.ImageField(upload_to='images/', blank=True, null=True)
    product_status = models.BooleanField(default=True)
     
    def __str__(self):
        return self.product_name
    
    
