# Generated by Django 5.1.1 on 2024-11-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0037_rename_order_details_return_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='offer',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]