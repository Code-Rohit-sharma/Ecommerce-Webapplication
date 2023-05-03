from django.contrib import admin
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataFieldValue, Product, ProductVariation, ProductReview, Cart, Order, OrderProduct, OrderStatus

# Register your models here.

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('id','product')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id','order','product_variation')

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order_product','from_status','to_status')


admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(CategoryMetaDataField)
admin.site.register(CategoryMetaDataFieldValue)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(ProductReview)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(OrderStatus,OrderStatusAdmin)
