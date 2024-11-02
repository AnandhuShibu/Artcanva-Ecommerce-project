from django.db import models

# Create your models here.

class Paint(models.Model):
    paint_type = models.CharField(max_length=200)
    paint_type_status = models.BooleanField(default=True)


class Art(models.Model):
    art_type = models.CharField(max_length=200)
    art_type_offer = models.PositiveIntegerField()
    art_type_status = models.BooleanField(default=True)
    
  
