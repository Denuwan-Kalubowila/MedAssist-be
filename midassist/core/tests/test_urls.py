"""This module representing a TestUrl Model"""
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from core.views import signup_view

class TestUrls(SimpleTestCase):
    """
    Test class for url testing 
    """
    def test_list_url(self):
        """Test method for url testing"""
        url=reverse('signup')
        print(resolve(url))