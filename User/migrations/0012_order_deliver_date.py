# Generated by Django 5.1.1 on 2024-10-21 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliver_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]