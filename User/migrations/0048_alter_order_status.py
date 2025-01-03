# Generated by Django 5.1.1 on 2024-11-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0047_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Returned', 'Returned'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
