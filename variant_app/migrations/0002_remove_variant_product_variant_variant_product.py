# Generated by Django 5.1.1 on 2024-10-09 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0004_product_product_status'),
        ('variant_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='product_variant',
        ),
        migrations.AddField(
            model_name='variant',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product_app.product'),
            preserve_default=False,
        ),
    ]