from django.db import models
import uuid

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.coupon_code:
            # Generate a unique coupon code if it doesn't exist
            self.coupon_code = str(uuid.uuid4()).replace('-', '')[:5].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.coupon_code
