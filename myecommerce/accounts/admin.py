from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import MyUser
from .models import UserAddress


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone','IC',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone','IC',)}),
    )


class UserAddressAdmin(admin.ModelAdmin):
       class Meta:
           model = UserAddress

admin.site.register(UserAddress , UserAddressAdmin)
admin.site.register(MyUser , CustomUserAdmin)