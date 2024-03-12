from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from users.models import User
    
class SignUpForm(UserCreationForm):
   class Meta:
      model = User 
      fields = ('username', 'first_name', 'last_name', 'email',)

# Allows a new user to register using template data, validates the data, and saves.  
# The user is able to be authenticated after creation. They are directed to 'login' to sign in.
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect(reverse("users:login"))
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})

# Authenticates user. If successful, redirects to the user's short_urls. Otherwise, remains on login screen.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect to a success page
                return redirect(reverse('short_url_list')) 
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout and redirects to register. 
def logout(request):
    auth_logout(request)
    return redirect(reverse("users:register")) 