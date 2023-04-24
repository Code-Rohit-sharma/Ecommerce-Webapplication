from django.db import models
from django.contrib.auth.models import User

# Create your models here.

AUTHORITY_CHOICES = (
    ('SELLER','SELLERY'),
    ('CUSTOMER','CUSTOMER')
)

class CustomizeUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    invalid_password_attempt = models.PositiveIntegerField(default=0)
    password_update_date = models.DateField()
    
class Role(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    authority = models.CharField(choices=AUTHORITY_CHOICES,max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.authority

class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
