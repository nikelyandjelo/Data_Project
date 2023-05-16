from django.db import models

class PaymentMethod(models.Model):
  name = models.CharField(max_length=50)

class IncomePaymentMethod(models.Model):
  name = models.CharField(max_length=50)

class Location(models.Model):
  name = models.CharField(max_length=50)


PAYMENT_CHOICES = [ ('cash', 'cash'),   
                    ('credit', 'credit card'),  
                    ('debit', 'debit card'),  
                    ('bank_transfer', 'bank transfer'),]

PAYMENT_CHOICES_INCOME = [ ('cash', 'cash'), 
                          ('card', 'card')]

LOCATION_CHOICES =[ ('canada', 'canada'),
                    ('usa', 'usa'), 
                    ('europe', 'europe')]

class Income(models.Model):
  date = models.DateField()
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.CharField(max_length=100)
  income_payment_method = models.ForeignKey(IncomePaymentMethod, on_delete=models.CASCADE, choices=PAYMENT_CHOICES_INCOME)
  

class Expense(models.Model):
  date = models.DateField()
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.CharField(max_length=100)
  payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE,choices=PAYMENT_CHOICES)
  location = models.ForeignKey(Location, on_delete=models.CASCADE, choices = LOCATION_CHOICES)

