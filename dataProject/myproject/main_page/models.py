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

CATEGORY_CHOICES_INCOME = [
    ('Work1', 'Work 1'),
    ('Work2', 'Work 2'),
    ('Work3', 'Work 3'),
    ('Foreign_income', 'Foreign Income'),
    ('Investments', 'Investments'),
]

CATEGORY_CHOICES_EXPENSE = [
    ('Fod', 'Food'),
    ('Clothes', 'Clothes'),
    ('Rent', 'Rent'),
    ('Another_expenses', 'Another Expenses'),
]


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=50, default='', choices=CURRENCY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    custom_category = models.CharField(max_length=50, blank=True)

    def get_category_display(self):
        if self.custom_category:
            return self.custom_category
        return dict(CATEGORY_CHOICES_INCOME).get(self.category)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=50, default='', choices=CURRENCY_CHOICES)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    custom_category = models.CharField(max_length=50, blank=True)

    def get_category_display(self):
        if self.custom_category:
            return self.custom_category
        return dict(CATEGORY_CHOICES_EXPENSE).get(self.category)
