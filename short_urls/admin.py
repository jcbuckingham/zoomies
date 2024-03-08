from django.contrib import admin
from .models import ShortURL

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_code', 'created_at')
    search_fields = ['original_url', 'short_code']
    list_filter = ('created_at',)

admin.site.register(ShortURL, ShortURLAdmin)
