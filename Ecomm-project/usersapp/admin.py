from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomizeUser,Role,UserRole,Address,Seller,Customer

# Register your models here.
class UserInline(admin.StackedInline):
    model = CustomizeUser
    can_delete = False
    verbose_name_plural = 'User Detail'

class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False
    extra = 1
    verbose_name_plural = 'Address'

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    extra = 1
    verbose_name_plural = 'user as Customer'

class CustomizeUserAdmin(UserAdmin):
    inlines = (UserInline,AddressInline,CustomerInline)
  
admin.site.register(Address)
admin.site.register(Seller)
admin.site.register(Customer)

admin.site.register(Role)
admin.site.register(UserRole)

admin.site.unregister(User)
admin.site.register(User,CustomizeUserAdmin)