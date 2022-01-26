from django.urls import include ,path ,re_path
from products import views
from carts import views as views2
from orders import views as views3
from accounts import views as views4
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from carts.models import Cart ,CartItem
from products.models import Product
from django.views.generic import TemplateView
admin.autodiscover()



urlpatterns = [


    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('s/', views.search, name='search'),
    path('products/' , views.all , name='all'),
    path('cart/' , views2.view, name='cart'),
    path('checkout/' , views3.checkout, name='checkout'),
    path('checkout/payment' , views3.direct_payment_view, name='direct_payment'),
    path('orders/' , views3.orders , name='user_orders'),
    path('accounts/profile/' , views4.account , name='profile'),
    path('accounts/logout/' , views4.logout_view , name='auth_logout'),
    path('accounts/login/' , views4.login_view , name='auth_login'),
    path('accounts/register' , views4.Registeration_view, name='auth_register'),
    path('accounts/update/' , views4.update_user_view, name='auth_update'),
    path('accounts/password/', views4.change_password, name='change_password'),
    path('accounts/check_email/', TemplateView.as_view(template_name="users/check.htm"), name='check_email'),
    path('accounts/invalid_link/', TemplateView.as_view(template_name="users/invalid.htm"), name='invalid'),
    path('ajax/add_user_address' , views4.Add_user_Address, name='ajax_add_user_address'),
    path('ajax/select_address' , views4.select_address, name='ajax_select_address'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views4.activate, name='activate'),
    re_path(r'^products/(?P<id>\d+)/$', views2.remove_from_cart , name ='remove_from_cart'),
    re_path(r'^addresses/(?P<id>\d+)/$', views4.delete_address , name ='delete_address'),
    re_path(r'^Update_address/(?P<id>\d+)/$', views4.update_address_view , name ='update_address'),
    re_path(r'^products/(?P<slug>[\w-]+)/$', views.single , name = 'single_product'),
    re_path(r'^wishlist_add/(?P<slug>[\w-]+)/$', views.add_to_wishlist , name = 'add_to_wishlist'),
    re_path(r'^wishlist_remove/(?P<slug>[\w-]+)/$', views.remove_from_wishlist , name = 'remove_from_wishlist'),
    re_path(r'^cart/(?P<slug>.[\w-]+)/$', views2.add_to_cart , name='add_to_cart'),
    re_path(r'^singletocart/(?P<slug>.[\w-]+)/$', views2.add_to_cart3 , name='add_to_cart3')

    #(?P<serial>\d+)  url using serial number.
]
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
