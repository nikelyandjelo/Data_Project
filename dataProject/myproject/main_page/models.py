from django.db import models
from django.contrib.auth.models import User

CURRENCY_CHOICES = [
  ('USD', 'USD'),
  ('EUR', 'EUR'),
  ('GBP', 'GBP'),
]

PAYMENT_METHOD_CHOICES = [
  ('Cash', 'Cash'),
  ('Credit Card', 'Credit Card'),
  ('Bank Transfer', 'Bank Transfer'),
]

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Income(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  date = models.DateField(max_length=50)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=50,default='',choices=CURRENCY_CHOICES)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

class Expense(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  date = models.DateField(max_length=50)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=50,default='',choices=CURRENCY_CHOICES)
  payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

