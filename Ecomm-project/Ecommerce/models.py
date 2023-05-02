from django.db import models
from usersapp.models import Seller, Customer
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class ParentCategory(models.Model):
    parent_category_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.parent_category_name


class Category(models.Model):
    parentcategory = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


class CategoryMetaDataField(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CategoryMetaDataFieldValue(models.Model):
    categorymetafield = models.ForeignKey(
        CategoryMetaDataField, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    values = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.categorymetafield.name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_canceleable = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=False)
    brand = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name+'-'+str(self.id)


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity_available = models.PositiveIntegerField()
    metadata = models.CharField(max_length=300)
    primary_image_field = models.ImageField(upload_to='images')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)


class ProductReview(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_wishlist_item = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer.user.username)


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('ONLINE', 'ONLINE'),
        ('CASH', 'CASH')
    )

    ADDRESS_LABEL = (
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_paid = models.PositiveIntegerField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_CHOICES,default='HOME',null=True,blank=True)
    customer_address_city = models.CharField(max_length=100)
    customer_address_state = models.CharField(max_length=100)
    customer_address_country = models.CharField(max_length=100)
    customer_address_address_line = models.CharField(max_length=150)
    customer_address_zip_code = models.PositiveIntegerField()
    customer_address_label = models.CharField(
        choices=ADDRESS_LABEL, max_length=100,default='HOME')

    def __str__(self):
        return str(self.customer.user.username)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order.customer.user.username)


class OrderStatus(models.Model):

    FROM_STATUS = (
        ('ORDER_PLACED', 'ORDER_PLACED'),
        ('CANCELED', 'CANCELED'),
        ('ORDER_REJECTED', 'ORDER_REJECTED'),
        ('ORDER_CONFIRMED', 'ORDER_CONFIRMED'),
        ('ORDER_SHIPPED', 'ORDER_SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('RETURN_REQUEST', 'RETURN_REQUEST'),
        ('RETURN_REJECTED', 'RETURN_REJECTED'),
        ('RETURN_APPROVED', 'RETURN_APPROVED'),
        ('PICK_UP_INITIATED', 'PICK_UP_INITIATED'),
        ('PICK_UP_COMPLETED', 'PICK_UP_COMPLETED'),
        ('REFUND_INITIATED', 'REFUND_INITIATED'),
        ('REFUND_COMPLETED', 'REFUND_COMPLETED')
    )

    TO_STATUS = (
        ('ORDER_CONFIRMED', 'ORDER_CONFIRMED'),
        ('ORDER_REJECTED', 'ORDER_REJECTED'),
        ('CLOSED', 'CLOSED'),
        ('CANCELED', 'CANCELED'),
        ('ORDER_SHIPPED', 'ORDER_SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('RETURN_REQUEST', 'RETURN_REQUEST'),
        ('RETURN_REJECTED', 'RETURN_REJECTED'),
        ('RETURN_APPROVED', 'RETURN_APPROVED'),
        ('PICK_UP_INITIATED', 'PICK_UP_INITIATED'),
        ('PICK_UP_COMPLETED', 'PICK_UP_COMPLETED'),
        ('REFUND_INITIATED', 'REFUND_INITIATED'),
        ('REFUND_COMPLETE', 'REFUND_COMPLETE'),
    )

    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    from_status = models.CharField(
        max_length=100, choices=FROM_STATUS, default='ORDER_PLACED')
    to_status = models.CharField(max_length=100, choices=TO_STATUS,default='ORDER_CONFIRMED')
    transition_notes_comment = models.CharField(max_length=150,default='nothing')
    transition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_product.order)
