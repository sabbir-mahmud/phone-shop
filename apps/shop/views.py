from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.context_processor import carts

from .models import Cart, Phone

User = get_user_model()


class Home(View):
    def get(self, request):
        phones = Phone.objects.all().order_by("-id")[:9]

        context = {
            "phones": phones
        }

        return render(request, 'shop/home.html', context)


class AddToCarT(View):
    def get(self, request, pk):
        phone = Phone.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.filter(
            Q(phone_id=phone.id) & Q(user_id=user.id)).exists()
        if cart:
            cart = Cart.objects.get(Q(phone_id=phone.id) & Q(user_id=user.id))
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(phone_id=phone, user_id=user, quantity=1)
        return redirect("/")


def get_all_carts(request):
    carts = Cart.objects.get(user_id=request.user.id)
    context = {
        "carts": carts
    }
    return render(request, 'shop/carts.html', context)


def remove_quantity(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.quantity -= 1
    cart.save()
    return redirect("/")


def remove_from_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect("/")
