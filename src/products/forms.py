from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Products, Order
from django.core.validators import MaxValueValidator, MinValueValidator 


class OrderUpdateForm(forms.ModelForm):
    quantity=forms.IntegerField(validators=[MinValueValidator(0)])
    class Meta :
        model = Order
        fields = ['quantity']

class ProductUpdateForm(forms.ModelForm):
    quantity_in_stock=forms.IntegerField(validators=[MinValueValidator(0)])
    image = forms.ImageField()
    class Meta :
        model = Order
        fields = ['quantity_in_stock' , 'image']



