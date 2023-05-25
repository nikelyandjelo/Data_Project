from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [ 'amount', 'description', 'currency']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [ 'amount',  'description', 'currency', 'payment_method']

