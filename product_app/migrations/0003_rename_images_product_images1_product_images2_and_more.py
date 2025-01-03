# Generated by Django 5.1.1 on 2024-10-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_product_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='images',
            new_name='images1',
        ),
        migrations.AddField(
            model_name='product',
            name='images2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='images3',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
