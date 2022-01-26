from django.db import models
from django.urls import reverse , NoReverseMatch
from django.conf import settings
from accounts.models import MyUser
import random
import string
# Create your models here.



def key_genrator(size = 10 , chars = string.ascii_uppercase + string.digits):
    theKey = "".join(random.choice(chars) for x in range(size))
    return theKey

class Product(models.Model):
    title = models.CharField(max_length = 30)
    describtion = models.TextField(null = True , blank = True )
    price = models.DecimalField(decimal_places = 2 , max_digits = 10 , default = 0.0)
    slug = models.SlugField(unique = True)
    timeStamp = models.DateTimeField(auto_now_add = True , auto_now = False)
    active = models.BooleanField(default = True)
    trending = models.BooleanField(default = False)


    def __str__(self):
        return self.title
    class Meta:
        unique_together = ('title','slug')
    def get_price(self):
        return self.price
    def get_absolute_url(self):
        return reverse('single_product' , kwargs ={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products/images')
    featured = models.BooleanField(default = False)
    thumbnail = models.BooleanField(default = False)

    def __str__(self):
        return self.product.title



class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager , self).filter(active = True).filter(category = 'size')

    def colors(self):
        return super(VariationManager , self).filter(active = True).filter(category = 'color')


Var_categories =(
     ('size' , 'size'),
     ('color' , 'color'),
    )




class Variation(models.Model):

    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    title = models.CharField(max_length = 30)
    category = models.CharField(max_length = 30 , choices = Var_categories ,default = 'size')
    image = models.ForeignKey(ProductImage,on_delete = models.CASCADE ,null = True , blank=True)
    price = models.DecimalField(decimal_places = 2 , max_digits = 10 , default = 0.0 , null = True)
    active = models.BooleanField(default = True)

    objects = VariationManager()



    def __str__(self):
        return self.title

    def getProduct_id(self):
        return self.product.id
    getProduct_id.short_description ='Product id'

    def getProduct_title(self):
        return self.product.title
    getProduct_title.short_description ='Product title'

    def getProduct_timestamp(self):
        return self.product.timeStamp
    getProduct_timestamp.short_description ='Product timeStamp'




class Wishlist(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    wished_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length = 15 , default = key_genrator)
    whishlist_slug = models.CharField(max_length=42,unique = True)
    added_date = models.DateTimeField(auto_now_add=True , auto_now = False)

    def getProduct_title(self):
        return self.product.title

    def __str__(self):
        return self.wished_product.title
