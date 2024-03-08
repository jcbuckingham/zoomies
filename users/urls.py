from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("detail/", views.index, name="detail"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]