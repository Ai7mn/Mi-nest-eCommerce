from django.contrib.auth import get_user_model
from django.db import models
from carts.models import Cart , CartItem
from accounts.models import UserAddress
from django.conf import settings
from django.utils.safestring import mark_safe
# Create your models here.

User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
      ("Unpaid" , "Unpaid"),
      ("Pending" , "Pending Payment Confirmation"),
      ("shipping" ,"shipping"),
      ("shipped" ,"shipped"),
)

Paymnet_Status = (
      ("Unpaid" , "Unpaid"),
      ("Unconfirmend" , "Pending payment confirmation"),
      ("Recived" ,"Payment Received"),
)


class Payment(models.Model):
    payment_slip = models.ImageField(upload_to = 'orders/paymentSlips' )
    paymnet_status =  models.CharField(max_length = 120 , choices = Paymnet_Status , default ="Unpaid")
    payment_slip_upload_time = models.DateTimeField(auto_now_add = True , auto_now = False)

    def __str__(self):
        return str(self.id)
    def get_slip(self):
        return   mark_safe('<a target ="_blank" href="../../../%s"><img src="../../../%s" width=150px; hight=auto;/></a>' % (self.payment_slip.url , self.payment_slip.url))


    get_slip.short_description = 'payment slip'





class Order(models.Model):
    user = models.ForeignKey(User , null = True , blank = True , on_delete = models.CASCADE)
    order_id =  models.CharField(max_length = 120 , default = "ABC", unique = True)
    cart = models.ForeignKey(Cart , on_delete = models.CASCADE)
    payment = models.OneToOneField(Payment , null = True , blank = True , on_delete = models.CASCADE)
    status = models.CharField(max_length = 120 , choices = STATUS_CHOICES , default ="Unpaid")
    address = models.ForeignKey(UserAddress , on_delete = models.CASCADE  , null = True , blank = True)
    sub_total = models.DecimalField(decimal_places = 2 , max_digits = 20 , default = 0.0)
    courier_company =  models.CharField(max_length = 120  , null = True , blank = True)
    tracking_number =  models.CharField(max_length = 120  , null = True , blank = True)
    shipping = models.DecimalField(decimal_places = 2 , max_digits = 20 , default = 15.00)
    final_total = models.DecimalField(decimal_places = 2 , max_digits = 20 , default = 0.0)
    timeStamp = models.DateTimeField(auto_now_add = True , auto_now = False)


    def __str__(self):
        return self.order_id

    def get_name(self):
        if self.address.reciver_name:
            return "%s" %(self.address.reciver_name)
        else:
            return "%s %s" %(self.user.first_name,self.user.last_name)

    def get_phone(self):
        if self.address.phone:
            return str(self.address.phone)
        else:
            return str(self.user.phone)


    def get_user_address(self):
        if self.address:
            return "%s , %s ,%s ,%s ,%s"  %(self.address.address ,self.address.city ,self.address.state , self.address.country , self.address.zipcode)
        else:
            return " There is no address yet."

    def get_payment_slip(self):
        if self.payment:
            return   mark_safe('<a target ="_blank" href="../../../%s"><img src="../../../%s" width=150px; hight=auto;/></a>' % (self.payment.payment_slip.url , self.payment.payment_slip.url))
        else:
            return 'unpaid'

    def get_payment_status(self):
        if self.payment:
            return self.payment.paymnet_status
        else:
            return 'unpaid'

    def get_payment_time(self):
        if self.payment:
            return str(self.payment.payment_slip_upload_time)
        else:
            return 'unpaid'

    def get_items(self):
        str1 = "<style> .item-table{font-family: arial, sans-serif;border-collapse: collapse; }</style>"
        str3 = "<table class='item-table' style='width:300px;'><tr class = 'mytr'><th class = 'mytth'>Product</th><th  class = 'mytth'>Quantity</th></tr>"
        total_str = str1  +str3
        items = CartItem.objects.filter(cart = self.cart)
        for item in items:
            str4 = "<tr class = 'mytr'> <td  class = 'mytd'>%s</td><td class = 'mytd' >%s</td> </tr>" % (item.product.title , item.quantity)
            total_str = total_str +str4
        total_str = total_str + "</table>"
        return mark_safe(total_str)

    get_payment_slip.short_description = 'payment slip'
    get_payment_status.short_description = 'payment status'
    get_payment_time.short_description = 'payment time'
    get_user_address.short_description = 'shipping Address'
    get_name.short_description = 'Reciver Name'
    get_phone.short_description = 'Phone'
    get_items.short_description = 'Ordered Items'
