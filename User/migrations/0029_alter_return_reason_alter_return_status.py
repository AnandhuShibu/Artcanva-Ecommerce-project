# Generated by Django 5.1.1 on 2024-11-04 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0028_alter_return_reason_alter_return_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='reason',
            field=models.CharField(default='Other', max_length=200),
        ),
        migrations.AlterField(
            model_name='return',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
