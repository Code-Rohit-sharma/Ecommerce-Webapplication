from django.db import models
from usersapp.models import Seller

# Create your models here.
class ParentCategory(models.Model):
    parent_category_name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.parent_category_name

class Category(models.Model):
    parentcategory = models.ForeignKey(ParentCategory,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

class CategoryMetaDataField(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CategoryMetaDataFieldValue(models.Model):
    categorymetafield = models.ForeignKey(CategoryMetaDataField,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    values = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.categorymetafield.name

class Product(models.Model):
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_canceleable = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=False)
    brand = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name        

class ProductVariation(models.Model):
    product_id = models.OneToOneField(Product,on_delete=models.CASCADE)
    quantity_available = models.PositiveIntegerField()
    metadata = models.CharField(max_length=300)
    primary_image_field = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_id.name