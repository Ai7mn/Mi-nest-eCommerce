import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse , NoReverseMatch
from django.conf import settings

from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from .models import Order ,Payment
from carts.models import Cart , CartItem
from .utils import id_genrator
from .forms import UploadPaymentForm
# Create your views here.


def orders(request):

    context = {}
    template = 'orders/user.html'

    return render(request , template ,context)


@login_required
def checkout(request) :
    try:
        cartId = request.session['cart_id']
        cart =  Cart.objects.get(id = cartId)
    except:
        cartId = None
        return HttpResponseRedirect(reverse("cart"))


    try:
        new_order = Order.objects.get(cart = cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_genrator()        #str(time.time())
        new_order.sub_total = cart.Sub_total
        new_order.final_total = cart.total
        new_order.save()
        request.session['order_id'] = new_order.order_id
    except:
        #assign error massage
        return HttpResponseRedirect(reverse("cart"))

    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    current_addresses = UserAddress.objects.filter(user = request.user)
  
    context = {"address_form" : address_form ,
    "current_addresses":current_addresses,
    }
    template = 'orders/checkout.htm'

    return render(request , template ,context)

@login_required
def direct_payment_view(request):
    form = UploadPaymentForm(request.POST ,  request.FILES or None)
    try:
        orderId = request.session['order_id']
        order = Order.objects.get(order_id = orderId)
    except:
        order = None
    if order is not None:
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.paymnet_status = 'Unconfirmend'
            new_payment.save()
            order.payment = new_payment
            order.status = 'Pending'
            order.save()
            return  HttpResponseRedirect(reverse("profile"))
    else:
        raise Http404              
    context = {
    "form" : form , "order" : order}
    return render(request , "orders/payment.htm" , context)