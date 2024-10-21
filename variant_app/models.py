from django.db import models
from product_app.models import Product

# Create your models here.

class Variant(models.Model):
    frame_size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    variant_status = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variants')
