# Generated by Django 5.1.1 on 2024-11-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0041_alter_order_coupon_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='item_coupon_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
