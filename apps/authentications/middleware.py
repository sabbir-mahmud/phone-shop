from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # If not authenticated, redirect to the login page
            login_url = reverse('login')  # Change 'login' to your actual login view name
            if request.path != login_url:
                return redirect(login_url)

        response = self.get_response(request)
        return response