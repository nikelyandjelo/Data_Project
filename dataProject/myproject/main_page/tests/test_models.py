from django.test import TestCase
from main_page.models import Income, Expense, Category
from django.contrib.auth.models import User

class IncomeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        category = Category.objects.create(
            user=user,
            name='Work1'
        )

        Income.objects.create(
            user=user,
            date='2023-03-03',
            amount=1000,
            currency='USD',
            category=category,
            custom_category='Smth'
        )

    def test_get_category_display(self):
        income = Income.objects.get(id=1)
        expected_category_display = income.custom_category
        self.assertEqual(income.get_category_display(), expected_category_display)


    def test_max_digits(self):
        income = Income.objects.get(id=1)
        max_digits = income._meta.get_field('amount').max_digits
        self.assertEqual(max_digits, 10)


    def test_max_length(self):
        income = Income.objects.get(id=1)
        max_length = income._meta.get_field('custom_category').max_length
        self.assertEqual(max_length, 50)


class ExpenseModelTest(TestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        category = Category.objects.create(
            user=user,
            name='Rent'
        )

        Expense.objects.create(
            id ='1',
            user=user,
            date='2023-03-04',
            amount=2500,
            currency='USD',
            payment_method = 'Credit card',
            category=category,
            custom_category='Smth2'
        )

    def test_get_category_display(self):
        expense = Expense.objects.get(id=1)
        expected_category_display = expense.custom_category
        self.assertEqual(expense.get_category_display(), expected_category_display)


    def test_max_digits(self):
        expense = Expense.objects.get(id=1)
        max_digits = expense._meta.get_field('amount').max_digits
        self.assertEqual(max_digits, 10)


    def test_max_length(self):
        expense = Expense.objects.get(id=1)
        max_length = expense._meta.get_field('custom_category').max_length
        self.assertEqual(max_length, 50)