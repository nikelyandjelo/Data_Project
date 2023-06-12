from django.test import TestCase
from main_page.forms import IncomeForm, ExpenseForm
from main_page.models import Category
from django.contrib.auth.models import User


class IncomeFormTest(TestCase):
    def test_income_form_labels(self):
        form = IncomeForm()
        self.assertEqual(form.fields['date'].label, 'Date')
        self.assertEqual(form.fields['amount'].label, 'Amount')
        self.assertEqual(form.fields['currency'].label, 'Currency')
        self.assertInHTML('<label for="id_category_name">Category name:</label>', form.as_p())
        self.assertEqual(form.fields['custom_category'].label, None)

    def test_income_form_widget_attrs(self):
        form = IncomeForm()
        self.assertEqual(form.fields['date'].widget.attrs['class'], 'datepicker')


class ExpenseFormTest(TestCase):
    def test_expense_form_labels(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['date'].label, 'Date')
        self.assertEqual(form.fields['amount'].label, 'Amount')
        self.assertEqual(form.fields['currency'].label, 'Currency')
        self.assertEqual(form.fields['payment_method'].label, 'Payment method')
        self.assertInHTML('<label for="id_category_name">Category name:</label>', form.as_p())
        self.assertEqual(form.fields['custom_category'].label, None )

    def test_expense_form_widget_attrs(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['date'].widget.attrs['class'], 'datepicker')
