# Generated by Django 2.2.16 on 2021-01-03 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20210103_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='value',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
