from django import forms
from .models import ShortURL

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
