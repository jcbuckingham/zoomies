from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
    
    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('users:register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration

    def test_login_view(self):
        response = self.client.post(reverse('users:register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users:logout'))

        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('users:login'), data={'username': self.user_data['username'], 'password': self.user_data['password1']})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        
    def test_logout_view(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect even if not logged in

