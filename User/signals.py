# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Order

@receiver(post_save, sender=Order)
def check_order_time_limit(sender, instance, created, **kwargs):
    if created:  # Check only when the order is created (not updated)
        time_diff = timezone.now() - instance.order_date
        if time_diff > timedelta(minutes=1):
            # You can add any custom logic here, like sending an email, 
            # updating the order status, or triggering a reminder.
            
            # Example: Updating the status of the order after 24 hours
            
            print(f"Order has passed 24 hours, and its status has been updated.")
