from django.test import TestCase, Client
from django.urls import reverse
from .models import ShortURL
from .forms import ShortURLForm

class ShortURLTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.short_url = ShortURL.objects.create(original_url='http://example.com', short_code='abc123')

    def test_short_url_creation(self):
        short_url = ShortURL.objects.get(original_url='http://example.com')
        self.assertEqual(short_url.short_code, 'abc123')

    def test_short_url_list_view(self):
        response = self.client.get(reverse('short_url_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'short_urls/list.html')

    def test_short_url_create_view(self):
        response = self.client.post(reverse('short_url_create'), {'original_url': 'http://example.com', 'short_code': 'abc123'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_short_url_update_view(self):
        short_url = ShortURL.objects.create(original_url='http://example.com/bnm', short_code='efg456')
        response = self.client.post(reverse('short_url_update', kwargs={'pk': short_url.pk}), {'original_url': 'http://updated.com', 'short_code': 'updated123'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        updated_short_url = ShortURL.objects.get(pk=self.short_url.pk)
        self.assertEqual(updated_short_url.original_url, 'http://updated.com')

    def test_short_url_delete_view(self):
        short_url = ShortURL.objects.create(original_url='http://delete_me.com', short_code='delete123')
        pk = short_url.pk
        response = self.client.post(reverse('short_url_delete', kwargs={'pk': pk}))
        print(response)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(ShortURL.objects.filter(pk=pk).exists())

    def test_short_url_form(self):
        form_data = {'original_url': 'http://example.com/abc', 'short_code': 'abc234'}
        form = ShortURLForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_short_url_form_invalid(self):
        form_data = {'original_url': '', 'short_code': 'abc456'}  # Invalid form data
        form = ShortURLForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_short_code_optional(self):
        # Test that short_code is optional
        form_data = {'original_url': 'http://example.com', 'short_code': ''}
        form = ShortURLForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_short_code_generation(self):
        # Test that short_code is generated if empty
        form_data = {'original_url': 'http://example.com', 'short_code': ''}
        form = ShortURLForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['short_code'])

    def test_invalid_url(self):
        # Test invalid URL
        form_data = {'original_url': 'invalidurl', 'short_code': ''}
        form = ShortURLForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('original_url', form.errors)
