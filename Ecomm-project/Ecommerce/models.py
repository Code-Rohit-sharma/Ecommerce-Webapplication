from django.db import models

# Create your models here.
class ParentCategory(models.Model):
    parent_category_name = models.CharField(max_length=100)

class Category(models.Model):
    parentcategory = models.ForeignKey(ParentCategory,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
