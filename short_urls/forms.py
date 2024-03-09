from django import forms
from django.db import IntegrityError
from .models import ShortURL
import random
import string

class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code']
        labels = {
            'original_url': 'Original URL',
            'short_code': 'Short Code'
        }
        widgets = {
            'original_url': forms.URLInput(attrs={'class': 'form-control'}),
            'short_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'short_code': {
                'unique': "This custom short code already exists. Try another or leave blank to generate a random short code."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_code'].required = False

    def save(self, commit=True, user=None):
        # Ensure that the user argument is provided
        if not user:
            raise ValueError("An authenticated user is required to create a short_url.")
        
        # Set the user_id
        self.instance.user_id = user.id

        try:
            return super().save(commit=commit)
        except IntegrityError:
            # Handle uniqueness constraint violation for short_code
            raise forms.ValidationError("The short code provided is not unique.")

    def clean_short_code(self):
        short_code = self.cleaned_data.get('short_code')

        # If a custom short_code is provided, return it as is
        if short_code:
            return short_code

        # Generate a random short_code
        length = 16
        chars = string.ascii_lowercase + string.digits
        short_code = ''.join(random.choice(chars) for _ in range(length))

        return short_code
