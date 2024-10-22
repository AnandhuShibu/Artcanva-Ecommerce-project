# Generated by Django 5.1.1 on 2024-10-19 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='User.address'),
            preserve_default=False,
        ),
    ]