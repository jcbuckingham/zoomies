from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

from users.models import User

class DetailView(generic.DetailView):
    model = get_user_model()
    template_name = "users/detail.html"

class IndexView(generic.ListView):
    template_name = "users/index.html"

    def get_queryset(self):
        """Return the first users."""
        return get_user_model().objects.order_by("id")[:20]
    
class SignUpForm(UserCreationForm):
   class Meta:
      model = User 
      fields = ('username', 'first_name', 'last_name', 'email',)

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

def logout(request):
    auth_logout(request)
    return redirect(reverse("users:login")) 
    
def index(request):
    user_list = get_user_model().objects.order_by("id")[:20]
    context = {
        "user_list": user_list,
    }
    return render(request, "users/index.html", context)

def detail(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    return render(request, "users/detail.html", {"user": user, "user_id": user.id})