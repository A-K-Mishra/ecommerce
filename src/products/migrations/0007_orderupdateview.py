# Generated by Django 2.2.16 on 2021-01-02 21:24

import django.contrib.auth.mixins
from django.db import migrations, models
import django.db.models.deletion
import django.views.generic.edit


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_delete_orderupdateview'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdateView',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Products')),
            ],
            bases=(django.contrib.auth.mixins.LoginRequiredMixin, django.contrib.auth.mixins.UserPassesTestMixin, django.views.generic.edit.UpdateView, 'products.products'),
        ),
    ]
