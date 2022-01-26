from django.shortcuts import render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from django.urls import reverse , NoReverseMatch
from django.contrib.auth.decorators import login_required
from .models import Product , Wishlist
from django.utils.text import slugify
# Create your views here.

def home(request) :
    products =  Product.objects.filter(trending=True)
    template = 'products/Home.htm'
    context = {'products' : products}
    
    return render(request , template ,context)

def search(request) :
       try:
         key = request.GET.get('keyword')
       except:
         key = None

       if key:
          products = Product.objects.filter(title__icontains = key)
          context = {'key' : key , 'products' : products}
          template = 'products/results.htm'
       else:
          template = 'Home.htm'
          context = {}

       return render(request , template ,context)

def all(request) :
    products =  Product.objects.all()
    mywishes = []
    if request.user.is_authenticated:
      for item in products:
        if Wishlist.objects.filter(user = request.user ,  wished_product=item):
          wished_product = Wishlist.objects.get(user = request.user ,  wished_product=item)
          mywishes.append(wished_product.wished_product)
          print(mywishes)
        context = {'products' : products , 'mywishes':mywishes}
    else:
      context = {'products' : products , 'mywishes':None}
    template = 'products/all.htm'
    return  render(request , template ,context)



def single(request , slug) :
    try:
         product = Product.objects.get(slug = slug)
         context = {'product' : product }
         template = 'products/single.htm'
         return  render(request , template ,context)
    except Exception as e:
        raise Http404

@login_required
def add_to_wishlist(request , slug):
    user = request.user
    product = Product.objects.get(slug = slug)
    wishlist_product = Wishlist.objects.create(user = user , wished_product=product)
    wishlist_product.whishlist_slug = slugify(wishlist_product.key+ str(wishlist_product))
    wishlist_product.save()
    return HttpResponseRedirect(reverse("all"))

@login_required
def remove_from_wishlist(request , slug):
    user = request.user
    product = Product.objects.get(slug = slug)
    wishlist_product = Wishlist.objects.get(user = user , wished_product = product)
    wishlist_product.delete()
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))
