from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ShortURL
from .forms import ShortURLForm

class ShortURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        # Register and login a user for all tests
        cls.client.post(reverse('users:register'), data=cls.user_data)
        cls.user = get_user_model().objects.get(username=cls.user_data['username'])
        cls.short_url = ShortURL.objects.create(original_url='http://example.com', short_code='abc123', user=cls.user)

    def setUp(self):
        self.client.post(reverse('users:login'), data={'username': self.user_data['username'], 'password': self.user_data['password1']})

    def test_short_url_creation(self):
        short_url = ShortURL.objects.get(short_code='abc123')
        self.assertEqual(short_url.original_url, 'http://example.com')

    def test_short_url_list_view(self):
        response = self.client.get(reverse('short_url_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'short_urls/list.html')

    def test_short_url_create_view(self):
        response = self.client.post(reverse('short_url_create'), {'original_url': 'https://example.com/something', 'short_code': 'shortcode123'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(response.url, "/api/short_urls")  # Redirected to short_urls index

    def test_short_url_update_view(self):
        short_url = ShortURL.objects.create(original_url='http://example.com/update_me', short_code='bcd456', user=self.user)
        response = self.client.post(reverse('short_url_update', kwargs={'pk': short_url.pk}), {'original_url': 'http://example.com/updated', 'short_code': 'updated123'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(response.url, "/api/short_urls")  # Redirected to short_urls index
        updated_short_url = ShortURL.objects.get(pk=short_url.pk)
        self.assertEqual(updated_short_url.original_url, 'http://example.com/updated')
        self.assertEqual(updated_short_url.short_code, 'updated123')

    def test_short_url_delete_view(self):
        short_url = ShortURL.objects.create(original_url='http://example.com/delete_me', short_code='delete123', user=self.user)
        pk = short_url.pk
        response = self.client.post(reverse('short_url_delete', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(response.url, "/api/short_urls")  # Redirected to short_urls index
        self.assertFalse(ShortURL.objects.filter(pk=pk).exists())

    def test_short_url_form_invalid_data(self):
        form_data = {'original_url': '', 'short_code': 'abc456'}
        form = ShortURLForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_short_code_generation(self):
        form_data = {'original_url': 'http://example.com', 'short_code': ''}
        form = ShortURLForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['short_code'])

    def test_invalid_url(self):
        form_data = {'original_url': 'invalidurl', 'short_code': ''}
        form = ShortURLForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('original_url', form.errors)

class ShortURLTestsAuthentication(TestCase):
    def setUp(self):
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='testpassword',
        )

    def test_short_url_list_view(self):
        response = self.client.get(reverse('short_url_list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/api/login/")  # Redirects to login because user is unauthenticated

    def test_short_url_create_view(self):
        response = self.client.post(reverse('short_url_create'), {'original_url': 'https://example.com/something', 'short_code': 'shortcode123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/api/login/")  # Redirects to login because user is unauthenticated
        # Ensure create did not take place
        self.assertFalse(ShortURL.objects.filter(short_code='shortcode123').exists())

    def test_short_url_update_view(self):
        short_url = ShortURL.objects.create(original_url='http://example.com/update_me', short_code='efg456', user=self.other_user)
        response = self.client.post(reverse('short_url_update', kwargs={'pk': short_url.pk}), {'original_url': 'http://example.com/updated', 'short_code': 'updated123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/api/login/")  # Redirects to login because user is unauthenticated
        # Ensure update did not take place
        updated_short_url = ShortURL.objects.get(pk=short_url.pk)
        self.assertEqual(updated_short_url.original_url, 'http://example.com/update_me')
        self.assertEqual(updated_short_url.short_code, 'efg456')

    def test_short_url_delete_view(self):
        short_url = ShortURL.objects.create(original_url='http://example.com/delete_me', short_code='delete123', user=self.other_user)
        pk = short_url.pk
        response = self.client.post(reverse('short_url_delete', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/api/login/")  # Redirects to login because user is unauthenticated
        # Ensure delete did not take place
        self.assertTrue(ShortURL.objects.filter(pk=pk).exists())
