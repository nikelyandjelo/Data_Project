from django.test import TestCase, RequestFactory, Client
from django.core import mail
from django.shortcuts import reverse
from decouple import config
from main_page.views import send_email
from main_page.models import Expense, Income, Category
from django.contrib.auth.models import User


class SendEmailTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.category = Category.objects.create(user=self.user, name='Work1')
        self.income = Income.objects.create(
            user=self.user,
            date='2023-03-03',
            amount=1000,
            currency='USD',
            category=self.category,
            custom_category='Smth'
        )
        self.expense = Expense.objects.create(
            user=self.user,
            date='2023-03-04',
            amount=2500,
            currency='USD',
            payment_method='Credit card',
            category=self.category,
            custom_category='Smth2'
        )

    def test_email_form(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('email_form'))
        self.assertEqual(response.status_code, 200)

    def test_send_email(self):
        form_data = {
            'to': 'veronika.shukhman@gmail.com',
        }
        request = self.factory.post(reverse('email_form'), data=form_data)
        request.user = self.user
        send_email(request)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Financial report")
        self.assertEqual(email.body, "Hello,\n\nHere is your financial report.")
        self.assertEqual(email.from_email, config('EMAIL_HOST_USER'))
        self.assertEqual(email.to, ['veronika.shukhman@gmail.com'])

        attachment1 = email.attachments[0]
        self.assertEqual(attachment1[0], 'income_report.csv')

        attachment2 = email.attachments[1]
        self.assertEqual(attachment2[0], 'expense_report.csv')


class IncomeListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category1 = Category.objects.create(name='Work1',  user=self.user)
        self.category2 = Category.objects.create(name='Work3',  user=self.user)

        self.income1 = Income.objects.create(
            user=self.user,
            date='2023-03-03',
            amount=1000,
            currency='USD',
            category=self.category1,
        )
        self.income2 = Income.objects.create(
            user=self.user,
            date='2023-04-03',
            amount=3000,
            currency='USD',
            category=self.category2,
        )
    
    def test_income_list(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('income_list'))
        self.assertEqual(response.status_code, 200)

    def test_income_deletion(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.post(reverse('income_list'), {'delete': self.income1.id})
        self.assertRedirects(response, reverse('income_list'))
        self.assertFalse(Income.objects.filter(id=self.income1.id).exists())


class ExpenseListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category1 = Category.objects.create(name='Rent',  user=self.user)
        self.category2 = Category.objects.create(name='Rent',  user=self.user)

        self.expense1 = Expense.objects.create(
            user=self.user,
            date='2023-03-04',
            amount=2500,
            currency='USD',
            payment_method = 'Credit card',
            category=self.category1,
        )
        self.expense2 = Expense.objects.create(
            user=self.user,
            date='2022-05-04',
            amount=3500,
            currency='USD',
            payment_method = 'Credit card',
            category=self.category2,
        )
    
    def test_expense_list(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)

    def test_expense_deletion(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.post(reverse('expense_list'), {'delete': self.expense1.id})
        self.assertRedirects(response, reverse('expense_list'))
        self.assertFalse(Income.objects.filter(id=self.expense1.id).exists())


class AddIncomeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Work1'
        )

    def test_add_income(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'date': '2023-03-03',
            'amount': 1000,
            'currency': 'USD',
            'category_name': 'Work1',
            'custom_category': 'Custom Category'   
        }
        response = self.client.post(reverse('add_income'), data=form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Income.objects.count(), 1) 
        income = Income.objects.first()
        self.assertEqual(income.user, self.user)  
        self.assertEqual(income.amount, 1000) 
        self.assertNotEqual(income.amount, 33) 
        self.assertEqual(income.currency, 'USD') 
        self.assertNotEqual(income.currency, 'UAH')
        self.assertNotEqual(income.category, 'Work1')
        self.assertEqual(income.custom_category, 'Custom Category') 


class AddExpenseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Rent'
        )

    def test_add_expense(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'date': '2023-05-06',
            'amount': 3000,
            'currency': 'USD',
            'payment_method' : 'Credit Card',
            'category_name': 'Rent',
            'custom_category': 'Custom Category', 
        }
        response = self.client.post(reverse('add_expense'), data=form_data)
        
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Expense.objects.count(), 1) 
        expense = Expense.objects.first()
        self.assertEqual(expense.user, self.user)  
        self.assertEqual(expense.amount, 3000) 
        self.assertEqual(expense.currency, 'USD')
        self.assertEqual(expense.payment_method, 'Credit Card')    
        self.assertEqual(expense.custom_category, 'Custom Category')    