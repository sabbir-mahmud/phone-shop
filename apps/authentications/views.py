from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from .forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        forms = RegisterForm()
        context = {
            "forms": forms
        }
        return render(request, "auth/register.html", context)

    def post(self, request):
        print(request.POST)
        forms = RegisterForm(request.POST)
        if forms.is_valid:
            forms.save()
            email = request.POST.get("email")
            password = request.POST.get("password")
            messages.info(request, "registered login")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "successfully login")
                return redirect("/")
        else:
            messages.error(request, "something went wrong")
            return redirect("register")


class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "successfully login")
            return redirect("/")
        else:
            messages.error(request, "email or password wrong")
            return redirect("login")


def logoutView(request):
    logout(request)
    return redirect("login")
