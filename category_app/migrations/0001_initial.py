# Generated by Django 5.1.1 on 2024-10-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art_type', models.CharField(max_length=200)),
                ('art_type_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paint_type', models.CharField(max_length=200)),
                ('paint_type_status', models.BooleanField(default=True)),
            ],
        ),
    ]
