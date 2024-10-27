from django.db import models
import uuid

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=0)
    expiry_date = models.DateField()

