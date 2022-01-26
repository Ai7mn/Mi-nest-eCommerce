from django.contrib import admin

# Register your models here.

from .models import Product , ProductImage , Variation , Wishlist

class ProductAdmin(admin.ModelAdmin):
       search_fields = ['title' ,'describtion']
       date_hierarchy = 'timeStamp'
       list_display = ['id', 'title' , 'price' , 'active' , 'timeStamp']
       list_editable = ['price' , 'active']
       list_filter = ['price' , 'active' ,'timeStamp']
       readonly_fields = ['timeStamp']
       prepopulated_fields = { "slug": ("title",)}
       class Meta:
           model = Product

class  VariationAdmin(admin.ModelAdmin):

       search_fields = ['getProduct_id','getProduct_title' ,'title' ]
       list_display = ['getProduct_id','getProduct_title' , 'category', 'title' , 'active','getProduct_timestamp' ]
       list_editable = ['active']
       list_filter = [ 'category','title' , 'active' ]
       readonly_fields = ['getProduct_timestamp']
       class Meta:
           model = Variation



class WishlistAdmin(admin.ModelAdmin):
       date_hierarchy = 'added_date'
       prepopulated_fields = { "whishlist_slug": ("key", "wished_product")}
       list_display = ['id', 'user','wished_product' , 'whishlist_slug' , 'added_date']
       readonly_fields = ['added_date']
       class Meta:
           model = Wishlist



admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Variation ,VariationAdmin)
admin.site.register(Wishlist ,WishlistAdmin)     