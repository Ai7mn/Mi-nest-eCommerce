from django.shortcuts import render
from django.contrib.auth import logout , login , authenticate
from django.http import Http404, HttpResponseRedirect , HttpResponse
from django.urls import reverse , NoReverseMatch
from django.contrib.auth.decorators import login_required
from .forms import LoginFrom , RegisterationForm ,UserAddressForm ,UserUpdateForm , AddressUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserAddress ,MyUser
from carts.models import Cart
from django.conf import settings
from orders.models import Order
from orders.utils import id_genrator
from products.models import Wishlist
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.

User = settings.AUTH_USER_MODEL

def logout_view(request):

    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):

    form = LoginFrom( request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username = username , password = password )
        login(request , user)
        return HttpResponseRedirect('/')
    context = {
    "form" : form
    }
    return render(request , "LoginForm.htm" , context)



def Registeration_view(request):

    form = RegisterationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit = False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        message = render_to_string('users/acc_active_email.htm', {
            'user':user, 
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            })
        mail_subject = 'Activate your Mi Nest account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponseRedirect('check_email')
    context = {
    "form" : form
    }
    return render(request , "signup.htm" , context)


def Add_user_Address(request):
    try:
        next_page = request.GET.get('next')
    except:
        next_page = None
    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid():
                new_address = form.save(commit = False)
                new_address.user = request.user
                new_address.save()
                if next_page is not None:
                    return HttpResponseRedirect(reverse(str(next_page)) + "?address_added=True")
    else:
        raise Http404

def select_address(request):
    if request.method == "POST":
        try:
            addrId = request.POST.get('shipping_address')
        except:
            addrId = None    
        if addrId is not None:
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
            except:
                return HttpResponseRedirect(reverse("cart"))
            select_address = UserAddress.objects.get(id=addrId)
            new_order.address = select_address
            new_order.save()
            del request.session['cart_id']
            del request.session['items_total']
            return HttpResponseRedirect(reverse("direct_payment"))
    else:
        return HttpResponseRedirect(reverse("checkout"))


def account(request):
    if request.user.is_authenticated:
        user = request.user
        addressess = UserAddress.objects.filter(user = user)
        orders = Order.objects.filter(user=user)
        wisheds = Wishlist.objects.filter(user = user)
        context = { "user" : user , "addressess": addressess , "wisheds":wisheds , "orders":orders}
        template = 'users/profile.htm'
        return render(request , template , context)
    else:
        return HttpResponseRedirect(reverse("auth_login"))


@login_required
def update_user_view(request):
    user = request.user
    form = UserUpdateForm(request.POST or None , instance=user)
    if form.is_valid():
        uesr = form.save(commit=False)
        user.save()
        return  HttpResponseRedirect(reverse("profile"))
    context = {
    "form" : form
    }
    return render(request , "users/edit_user.htm" , context)

@login_required
def update_address_view(request , id):
    address = UserAddress.objects.get(id = id)
    form = AddressUpdateForm(request.POST or None , instance=address)
    if form.is_valid():
        address = form.save(commit=False)
        address.save()
        return  HttpResponseRedirect(reverse("profile"))
    context = {
    "form" : form
    }
    return render(request , "users/edit_user.htm" , context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse("auth_login"))
        else:
            return HttpResponseRedirect(reverse("change_password"))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_user.htm', {
        'form': form
    })

@login_required
def delete_address(request , id):
    address  = UserAddress.objects.get(id = id)
    address.delete()
    return HttpResponseRedirect(reverse("profile"))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect('invalid')