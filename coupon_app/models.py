from django.db import models
from django.contrib.auth.models import User
import uuid

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=0)
    expiry_date = models.DateField()

class Coupon_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Coupon_user')
    coupon_used = models.ForeignKey(Coupons, on_delete=models.CASCADE, related_name='Coupon_user')