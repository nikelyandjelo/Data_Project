from django import forms
from .models import Income, Expense, Category

class IncomeForm(forms.ModelForm):
    category_name = forms.CharField(max_length=50)
    class Meta:
        model = Income
        fields = [ 'date','amount', 'currency']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def save(self, commit=True):
        category_name = self.cleaned_data.get('category_name')
        category, _ = Category.objects.get_or_create(name=category_name, user=self.instance.user)
        self.instance.category = category
        return super().save(commit=commit)

class ExpenseForm(forms.ModelForm):
    category_name = forms.CharField(max_length=50)
    class Meta:
        model = Expense
        fields = [ 'date','amount', 'currency', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def save(self, commit=True):
        category_name = self.cleaned_data.get('category_name')
        category, _ = Category.objects.get_or_create(name=category_name, user=self.instance.user)
        self.instance.category = category
        return super().save(commit=commit)

