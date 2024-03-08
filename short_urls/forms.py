from django import forms
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_code'].required = False

    def clean_short_code(self):
        short_code = self.cleaned_data.get('short_code')

        # If short_code is provided, return it as is
        if short_code:
            return short_code

        # Generate a random short_code
        length = 16
        chars = string.ascii_lowercase + string.digits
        short_code = ''.join(random.choice(chars) for _ in range(length))

        return short_code
