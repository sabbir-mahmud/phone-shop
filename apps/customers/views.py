from django.shortcuts import render
from django.views import View


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile/profile.html')


class SettingsView(View):
    def get(self, request):
        return render(request, 'profile/settings.html')


class OrderView(View):
    def get(self, request):
        return render(request, 'profile/orders.html')
