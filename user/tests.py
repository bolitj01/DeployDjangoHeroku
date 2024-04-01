from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewTests(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.test_username = 'testuser'
        self.test_password = 'securepassword123'

    def test_register_user(self):
        # Test registration process
        response = self.client.post(reverse('create_user'), {
            'username': self.test_username,
            'password': self.test_password,
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.test_username).exists())

    def test_login_user(self):
        # Create a user for testing login
        User.objects.create_user(username=self.test_username, password=self.test_password)
        # Login
        response = self.client.post(reverse('login'), {
            'username': self.test_username,
            'password': self.test_password,
        }, follow=True)
        # Check request.data contains "logged in" message
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged in', response.data)
        
        # Check that the user is logged in
        response = self.client.get(reverse('is_logged_in'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'is_logged_in': True,
            'username': self.test_username,
        }, response.data)

    def test_logout_user(self):
        # Create a user for testing login
        User.objects.create_user(username=self.test_username, password=self.test_password)
        # Login
        response = self.client.post(reverse('login'), {
            'username': self.test_username,
            'password': self.test_password,
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged out', response.data)
        
