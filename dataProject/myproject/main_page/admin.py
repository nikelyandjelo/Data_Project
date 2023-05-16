from django.contrib import admin
from .models import PaymentMethod, Location, Income, Expense

admin.site.register(PaymentMethod)
admin.site.register(Location)
admin.site.register(Income)
admin.site.register(Expense)

