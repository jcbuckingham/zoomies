from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from functools import wraps

from users.models import User

# Decorator for checking if the user is authenticated
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("users:login"))
        return view_func(request, *args, **kwargs)
    return wrapper

# Decorator for redirecting authenticated users
def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("short_url_list"))
        return view_func(request, *args, **kwargs)
    return wrapper

# Decorator for processing POST requests
def process_post(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return view_func(request, *args, **kwargs)
        return redirect(reverse("short_url_list"))
    return wrapper

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

@swagger_auto_schema(
    request_body=SignUpForm,
    responses={
        200: openapi.Response('Successful registration')
    },
    operation_summary="Register a new user",
    operation_description="This API endpoint registers a new user."
)
@process_post
def register(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("users:login"))
    return render(request, 'users/register.html', {'form': form})

@swagger_auto_schema(
    request_body=AuthenticationForm,  # Use your AuthenticationForm serializer
    responses={
        200: openapi.Response('Successful login')
    },
    operation_summary="Login user",
    operation_description="This API endpoint logs in a user."
)
@process_post
@redirect_authenticated_user
def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('short_url_list')) 
    return render(request, 'users/login.html', {'form': form})

@swagger_auto_schema(
    responses={
        200: openapi.Response('Successful logout')
    },
    operation_summary="Logout user",
    operation_description="This API endpoint logs out a user."
)
def logout(request):
    auth_logout(request)
    return redirect(reverse("users:login")) 
