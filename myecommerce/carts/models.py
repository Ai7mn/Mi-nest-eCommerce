from django.db import models

from products.models import Product , Variation
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey('Cart' , null = True , blank = True , on_delete = models.CASCADE)
    product = models.ForeignKey(Product,  on_delete = models.CASCADE)
    variations = models.ManyToManyField(Variation)
    quantity = models.IntegerField(default = 1)
    line_total = models.DecimalField(default = 0.0 ,decimal_places = 2 , max_digits = 20 )
    timeStamp = models.DateTimeField(auto_now_add = True , auto_now = False)


    def __str__(self):
       try:
           return str(self.cart.id)
       except:
           return self.product.title



class Cart(models.Model):

    Sub_total = models.DecimalField(decimal_places = 2 , max_digits = 20 , default = 0.0)
    total = models.DecimalField(decimal_places = 2 , max_digits = 20 , default = 0.0)
    timeStamp = models.DateTimeField(auto_now_add = True , auto_now = False)
    active = models.BooleanField(default = True)


    def __str__(self):
        return str(self.id)
