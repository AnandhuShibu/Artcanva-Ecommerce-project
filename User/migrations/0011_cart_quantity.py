# Generated by Django 5.1.1 on 2024-10-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
