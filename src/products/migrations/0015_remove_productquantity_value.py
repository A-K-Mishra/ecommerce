# Generated by Django 2.2.16 on 2021-01-03 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20210103_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productquantity',
            name='value',
        ),
    ]
