from django.contrib import admin
from .models import Products,Order,ProductQuantity
# Register your models here.
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(ProductQuantity)