# Generated by Django 5.1.1 on 2024-11-23 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0044_userinformations_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformations',
            name='email',
        ),
    ]
