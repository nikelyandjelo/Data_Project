from django.db import models

from django.contrib.auth.models import User
from main_page.models import Income, Expense


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    incomes = models.ManyToManyField(Income)
    expenses = models.ManyToManyField(Expense)
