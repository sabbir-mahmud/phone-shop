from django.middleware.csrf import get_token
from django.shortcuts import redirect


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/auth/login/" or request.path == "/auth/register/" or request.path == "/" or request.path == "/payment/ssl-commerce/callback/":
            response = self.get_response(request)
            return response

        if not request.user.is_authenticated:
            if request.path != "/auth/login/":
                return redirect("login")

        response = self.get_response(request)
        return response
