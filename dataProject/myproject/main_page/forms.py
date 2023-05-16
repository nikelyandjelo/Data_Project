from django import forms
from .models import Income
from .models import Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('date', 'amount', 'description','income_payment_method')

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('date', 'amount', 'description','payment_method','location')



