from django.test import TestCase
from django.contrib.auth.models import User
from main_page.utils import process_category, convert_to_csv

class ProcessCategoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_process_category_with_custom_category(self):
        custom_category = 'Custom Category'
        category = process_category('Rent', custom_category, self.user)

        self.assertIsNotNone(category)
        self.assertEqual(category.name, custom_category)
        self.assertEqual(category.user, self.user)

    def test_process_category_with_category(self):
        category_name = 'Rent'
        category = process_category(category_name, None, self.user)

        self.assertIsNotNone(category)
        self.assertEqual(category.name, category_name)
        self.assertEqual(category.user, self.user)