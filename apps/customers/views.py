from django.shortcuts import render
from django.views import View

from apps.shop.models import Order


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile/profile.html')


class SettingsView(View):
    def get(self, request):
        return render(request, 'profile/settings.html')


class OrderView(View):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user)
        context = {"orders": orders}
        return render(request, 'orders/orders.html', context)
