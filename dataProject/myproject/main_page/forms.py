from django import forms
from .models import Income, Expense, Category, CATEGORY_CHOICES_INCOME, CATEGORY_CHOICES_EXPENSE

def process_category(category_name, custom_category, user):
    category = None
    if custom_category:
        category, _ = Category.objects.get_or_create(name=custom_category, user=user)
    elif category_name:
        category, _ = Category.objects.get_or_create(name=category_name, user=user)
    return category

class IncomeForm(forms.ModelForm):
    category_name = forms.ChoiceField(choices = CATEGORY_CHOICES_INCOME)
    custom_category = forms.CharField(max_length = 50, required = False)
    class Meta:
        model = Income
        fields = [ 'date','amount', 'currency']
        widgets = {
            'date': forms.DateInput(attrs = {'class': 'datepicker', 'autocomplete': 'off', 'id': 'income_date'}),
            'custom_category': forms.TextInput(attrs = {'autocomplete': 'off'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IncomeForm, self).__init__(*args, **kwargs)
        # if request.user:
        #     self.fields['custom_category'].widgets.choices = []
        
class ExpenseForm(forms.ModelForm):
    category_name = forms.ChoiceField(choices = CATEGORY_CHOICES_EXPENSE)
    custom_category = forms.CharField(max_length = 50, required = False)
    class Meta:
        model = Expense
        fields = [ 'date','amount', 'currency', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs = {'class': 'datepicker'}),
            'custom_category': forms.TextInput(attrs = {'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
