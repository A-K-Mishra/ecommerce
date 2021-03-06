# Generated by Django 2.2.16 on 2021-01-05 08:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20210104_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='item_pics'),
        ),
        migrations.AddField(
            model_name='products',
            name='quantity_in_stock',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
