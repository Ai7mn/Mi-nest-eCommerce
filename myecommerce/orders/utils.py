import string
import random
from .models import Order

def id_genrator(size = 11 , chars = string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))

    try:
         order = Order.objects.get(order_id = the_id)
         id_genrator()
    except Order.DoesNotExist:
         return the_id
