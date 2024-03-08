from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access without authentication for register and login
        if request.path == reverse('users:login'):
            return self.get_response(request)
        
        if request.path == reverse('users:register'):
            return self.get_response(request)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page
            return redirect(reverse('users:login')) 

        response = self.get_response(request)
        return response
