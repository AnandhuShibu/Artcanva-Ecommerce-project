# Generated by Django 5.1.1 on 2024-11-11 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0038_order_details_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
