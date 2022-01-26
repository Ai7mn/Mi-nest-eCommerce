from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse , NoReverseMatch



from products.models import Product , Variation
from .models import Cart , CartItem
# Create your views here.


def view(request) :
    try:
        cartId = request.session['cart_id']
        cart =  Cart.objects.get(id = cartId)
    except:
        cartId = None


    if cartId:
        context = {'cart': cart }
        new_total=0
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * float(item.quantity)
            new_total += line_total

        request.session['items_total'] = cart.cartitem_set.count()
        cart.Sub_total = new_total
        cart.total = cart.Sub_total + 15 
        cart.save()
    else:
        empty_massage = " your cart is empty , plaese contine shopping. "
        context = {"empty": True , "empty_massage" : empty_massage }

    template = 'cart/view.htm'

    return render(request , template ,context)





def remove_from_cart(request , id):
    try:
        cartId = request.session['cart_id']
        cart =  Cart.objects.get(id = cartId)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cartitem  = CartItem.objects.get(id = id)
    cartitem.delete()
    #cartitem.cart = None
    #cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

def add_to_cart2(request , slug):
    request.session.set_expiry(1800)
    try:
        cartId = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cartId = new_cart.id

    cart =  Cart.objects.get(id = cartId)
    product = Product.objects.get(slug = slug)

    product_var = [] # product variation
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
              v = Variation.objects.get(id = val)
              product_var.append(v.id)
            except:
              pass

        cart_item  = CartItem.objects.create(cart = cart ,product = product )
        if len(product_var) > 0:
            cart_item.variations.add(product_var[0])
            cart_item.variations.add(product_var[1])

        cart_item.quantity = qty
        cart_item.save()
        request.session['items_total'] = cart.cartitem_set.count()

        return HttpResponseRedirect(reverse("home"))

    return HttpResponseRedirect(reverse("cart"))



def add_to_cart(request , slug):
    request.session.set_expiry(84600)
    try:
        cartId = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cartId = new_cart.id

    if request.method == "POST":
        qty = request.POST['quantity']
    else:
        qty = 1
    cart =  Cart.objects.get(id = cartId)
    product = Product.objects.get(slug = slug)
    cart_item  = CartItem.objects.create(cart = cart , product = product)
    cart_item.quantity = qty
    cart_item.line_total = product.price * int(qty)
    print(qty)
    cart_item.save()
    request.session['items_total'] = cart.cartitem_set.count()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def add_to_cart3(request , slug):
    request.session.set_expiry(84600)
    try:
        cartId = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cartId = new_cart.id

    if request.method == "POST":
        qty = request.POST['quantity']
    else:
        qty = 1
    cart =  Cart.objects.get(id = cartId)
    product = Product.objects.get(slug = slug)
    cart_item  = CartItem.objects.create(cart = cart , product = product)
    cart_item.quantity = qty
    cart_item.line_total = product.price * int(qty)
    print(qty)
    cart_item.save()
    request.session['items_total'] = cart.cartitem_set.count()
    return HttpResponseRedirect(reverse("all"))