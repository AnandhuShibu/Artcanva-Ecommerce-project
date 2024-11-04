# Generated by Django 5.1.1 on 2024-11-04 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0026_alter_return_reason_alter_return_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='reason',
            field=models.CharField(choices=[('damaged', 'Damaged Product'), ('wrong_item', 'Wrong Item Sent'), ('not_satisfied', 'Not Satisfied with Product'), ('other', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='return',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('request', 'Request'), ('approve', 'Approve')], default='pending', max_length=10),
        ),
    ]
