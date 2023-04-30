from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + " --> " + self.receiver.username + " = " + str(self.amount)