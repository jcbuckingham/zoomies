from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Allow users to login.
    path('login/', views.login, name='login'),

    # Allow users to logout.
    path('logout/', views.logout, name='logout'),

    # Allow new users to register.
    path('register/', views.register, name='register'),
]