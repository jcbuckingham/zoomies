from django.shortcuts import redirect
from django.urls import reverse
AUTH_NOT_REQUIRED_PATHS = [
    reverse('users:login'),
    reverse('users:register'),
    reverse('schema-swagger-ui'),
    reverse('schema-redoc'),
    reverse('openapi-schema'),
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access without authentication for register, login, and anything outside of the /api scope
        # which we will attempt to map to a short_url
        if request.path in AUTH_NOT_REQUIRED_PATHS or \
           not request.path.startswith('/api'):
            return self.get_response(request)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page
            return redirect(reverse('users:login')) 

        response = self.get_response(request)
        return response
