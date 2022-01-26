
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser



class MyUser(AbstractUser):
    phone = models.CharField(max_length=12 , unique=True)
    IC = models.CharField(max_length=15 , unique=True)

    def __str__(self):
       return str(self.username)



my_states =(
     ('Johor' , 'Johor'),
     ('Kedah' , 'Kedah'),
     ('Kelantan' , 'Kelantan'),
     (' Kuala Lumpur' , ' Kuala Lumpur'),
     ('Labuan' , 'Labuan'),
     ('Malacca' , 'Malacca'),
     ('Negeri Sembilan' , 'Negeri Sembilan'),
     ('Pahang' , 'Pahang'),
     ('Perak' , 'Perak'),
     ('Perlis' , 'Perlis'),
     ('Penang' , 'Penang'),
     ('Putrajaya' , 'Putrajaya'),
     ('Sabah' , 'Sabah'),
     ('Sarawak' , 'Sarawak'),
     ('Selangor' , 'Selangor'),
     ('Terengganu' , 'Terengganu'),

    )

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,  on_delete = models.CASCADE)
    reciver_name = models.CharField(max_length=120 , null = True , blank = True )
    phone = models.CharField(max_length=12 , null = True , blank = True )
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120 ,null = True , blank = True )
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120 ,null = True, choices=my_states , blank = True )
    country = models.CharField(max_length=120 )
    zipcode = models.CharField(max_length=20)
    shipping = models.BooleanField(default = True)
    billing =  models.BooleanField(default = False)
    timeStamp = models.DateTimeField(auto_now_add = True , auto_now = False)

    def __str__(self):
        return str(self.id)

    def get_address(self):
        return "%s , %s ,%s ,%s ,%s"  %(self.address ,self.city ,self.state , self.country , self.zipcode)
