from django import forms
from .models import Income, Expense, Category, CATEGORY_CHOICES_INCOME, CATEGORY_CHOICES_EXPENSE


class IncomeForm(forms.ModelForm):
    category_name = forms.ChoiceField(choices=CATEGORY_CHOICES_INCOME)
    custom_category = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Income
        fields = ['date', 'amount', 'currency']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 
                                           'autocomplete': 'off', 
                                           'id': 'income_date'}
                                    ),
            'custom_category': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(IncomeForm, self).__init__(*args, **kwargs)


class ExpenseForm(forms.ModelForm):
    category_name = forms.ChoiceField(choices=CATEGORY_CHOICES_EXPENSE)
    custom_category = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Expense
        fields = ['date', 'amount', 'currency', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 
                                           'autocomplete': 'off', 
                                           'id': 'expense_date'}
                                    ),
            'custom_category': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)


class EmailForm(forms.Form):
    to = forms.EmailField()