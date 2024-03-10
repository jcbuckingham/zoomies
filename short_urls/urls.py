from django.urls import path
from . import views

urlpatterns = [
    # List all short URLs
    path('', views.short_url_list, name='short_url_list'),

    # Create a new short URL
    path('create/', views.short_url_create, name='short_url_create'),

    # Update a specific short URL
    path('<int:pk>/update/', views.short_url_update, name='short_url_update'),

    # Delete a specific short URL
    path('<int:pk>/delete/', views.short_url_delete, name='short_url_delete'),
]
