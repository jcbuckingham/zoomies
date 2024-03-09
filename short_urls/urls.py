from django.urls import path, re_path
from . import views

urlpatterns = [
    # List all short URLs
    re_path(r'^short_urls/?$', views.short_url_list, name='short_url_list'),

    # Create a new short URL
    path('short_urls/create/', views.short_url_create, name='short_url_create'),

    # Update a specific short URL
    path('short_urls/<int:pk>/update/', views.short_url_update, name='short_url_update'),

    # Delete a specific short URL
    path('short_urls/<int:pk>/delete/', views.short_url_delete, name='short_url_delete'),
]
