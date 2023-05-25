from django.contrib import admin
from .models import  Income, Expense
from registration.models import UserProfile

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(UserProfile)