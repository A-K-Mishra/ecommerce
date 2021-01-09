from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator 


# Create your models here.
class Products(models.Model ):
    name = models.CharField( max_length = 200)
    description = models.TextField()
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits = 10 , decimal_places =2  )
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)] , default=0)
    image = models.ImageField( default = 'default.png' , upload_to = 'item_pics')

    def __str__(self):
        return self.name
    def save(self ):
        super().save()

        img = Image.open(self.image.path)
        
        if( img.height >300 or img.width > 300):
            output_size =(300 , 300)
            img.thumbnail (output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-products' ,  kwargs={'username':self.seller.username})

class ProductQuantity(models.Model ) :
    product = models.ForeignKey( Products ,  null=True, blank=True ,on_delete = models.CASCADE  )
    key = models.CharField(max_length = 240 )
    value = models.IntegerField(validators=[MinValueValidator(0)] , default=0)

class Order(models.Model ):
    buyer = models.ForeignKey(User , on_delete = models.CASCADE)
    items = models.ManyToManyField( ProductQuantity , blank = True , default=[] )
    date_ordered = models.DateTimeField(default = timezone.now)
    confirm_order = models.BooleanField(default = False )
    quantity = models.IntegerField(validators=[MinValueValidator(0)] , default=0)
    # add a dict field to incorporate quantity with added product's id as keys
    def get_absolute_url(self):
        return reverse('order-detail' , kwargs={'pk':self.pk} )
    


