"""
Test for core module
"""
from django.test import TestCase
from .models import User


class UserModelTestCase(TestCase):
    """Test Case Class"""
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'John',
            'age': 32,
            'phone_number':'1234567890'
        }

    def test_create_user(self):
        """Method for test_create_user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertEqual(user.age, self.user_data['age'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_doctor)

    def test_create_superuser(self):
        """Method for test_create_super_user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertEqual(user.age, self.user_data['age'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_doctor)


    def test_create_user_without_email(self):
        """Method for test_create_user_email"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', first_name='John', last_name='Doe')
