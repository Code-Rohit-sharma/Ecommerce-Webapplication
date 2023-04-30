from django.contrib import admin
from .models import ParentCategory,Category,CategoryMetaDataField,CategoryMetaDataFieldValue,Product,ProductVariation

# Register your models here.
admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(CategoryMetaDataField)
admin.site.register(CategoryMetaDataFieldValue)
admin.site.register(Product)
admin.site.register(ProductVariation)