from django.db import models
from django.contrib.auth.models import User

# Create your models here.

AUTHORITY_CHOICES = (
    ('SELLER', 'SELLER'),
    ('CUSTOMER', 'CUSTOMER')
)


class CustomizeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    invalid_password_attempt = models.PositiveIntegerField(default=0)
    password_update_date = models.DateField()


class Role(models.Model):
    authority = models.CharField(
        choices=AUTHORITY_CHOICES, max_length=50, default='CUSTOMER')

    def __str__(self):
        return self.authority


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+' '+self.role.authority


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gst = models.IntegerField()
    company_contact = models.PositiveBigIntegerField()
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.BigIntegerField()
    alternate_contact = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    LABEL_CHOICES = (
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE'),
        ('OTHER', 'OTHER')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address_line = models.TextField()
    zip_code = models.PositiveIntegerField()
    label = models.CharField(
        max_length=100, choices=LABEL_CHOICES, default='HOME')

    def __str__(self):
        return self.user.username

