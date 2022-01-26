from django.contrib import admin

from .models import Order , Payment
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
	search_fields = ['order_id' ,]
	date_hierarchy = 'timeStamp'
	list_display = ['order_id', 'get_payment_slip' , 'get_payment_status', 'get_payment_time', 'status' , 'tracking_number','get_name','get_phone' ,'get_user_address' ,   'courier_company' , 'get_items', 'sub_total' ,'final_total' , 'timeStamp']
	list_editable = ['status' , 'tracking_number', 'courier_company']
	# list_display_links  = ['order_id' , 'get_payment_slip']
	list_filter = ['status', 'courier_company' ,'timeStamp']
	readonly_fields = ['timeStamp']
	class Meta:
		model = Order

class PaymentAdmin(admin.ModelAdmin):
	search_fields = ['id' ,]
	date_hierarchy = 'payment_slip_upload_time'
	list_display = ['id', 'paymnet_status' , 'get_slip', 'payment_slip_upload_time']
	list_editable = ['paymnet_status']
	list_filter = ['paymnet_status', 'payment_slip_upload_time']
	readonly_fields = ['payment_slip_upload_time']
	class Meta:
		model = Payment

admin.site.register(Order , OrderAdmin)
admin.site.register(Payment , PaymentAdmin )
