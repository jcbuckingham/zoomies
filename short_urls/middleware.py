from django.shortcuts import redirect
from django.urls import reverse

# Whitelisted paths that do not require authentication
AUTH_NOT_REQUIRED_PATHS = [
    reverse('users:login'),
    reverse('users:register'),
    reverse('openapi-schema'),
]

# This runs before each request to ensure global authentication except for whitelisted paths
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access without authentication for whitelisted paths, and anything outside
        # of the /api scope which we will attempt to map to a short_url
        if request.path in AUTH_NOT_REQUIRED_PATHS or \
           not request.path.startswith('/api'):
            return self.get_response(request)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page
            return redirect(reverse('users:login')) 

        response = self.get_response(request)
        return response
