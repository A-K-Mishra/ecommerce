# Generated by Django 2.2.16 on 2021-01-03 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20210103_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Products'),
        ),
    ]
