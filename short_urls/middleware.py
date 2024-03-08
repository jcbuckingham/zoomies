import re
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access without authentication for register, login, and anything outside of the /api scope
        # which we will attempt to map to a short_url
        if request.path == reverse('users:login') or \
           request.path == reverse('users:register') or \
           not re.match(r'^\/api\/.*', request.path):
            return self.get_response(request)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page
            return redirect(reverse('users:login')) 

        response = self.get_response(request)
        return response
