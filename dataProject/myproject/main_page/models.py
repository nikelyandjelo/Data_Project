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
class Income(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  date = models.DateField(max_length=50)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  currency = models.CharField(max_length=50,default='',choices=CURRENCY_CHOICES)

class Expense(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  date = models.DateField(max_length=50)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField(max_length=50)
  currency = models.CharField(max_length=50,default='',choices=CURRENCY_CHOICES)
  payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

