import json
from decimal import Decimal

import stripe
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_python.payment import SSLCSession

from .models import Cart, DeliveryAddress, Order, Payment, Phone

stripe.api_key = "sk_test_51L0hxlEZlpATTp015WVNZvrzVgm1NSJpOgyGwploURgse2aEcf3PpIS1gCuu7gbWG0xf6QTXKAUsSVNxZUCSQAgG00H5nfUUcD"

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
            cart.sub_total = cart.phone_id.discount_price * cart.quantity
            cart.save()
        else:
            Cart.objects.create(phone_id=phone, user_id=user, quantity=1)
        return redirect('carts')


class Get_all_carts(View):
    def get(self, request):
        carts = Cart.objects.filter(user_id=request.user.id)
        context = {
            "carts": carts
        }
        return render(request, 'shop/carts.html', context)


def remove_quantity(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.quantity -= 1
    cart.sub_total = cart.phone_id.discount_price * cart.quantity
    cart.save()
    return redirect("carts")


def remove_from_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect("carts")


def generatePayment(request):
    if request.method == "POST":
        carts = json.loads(request.POST.get("carts"))
        amount = 0
        payment = Payment()
        payment.user_id = request.user
        payment.delivery = DeliveryAddress.objects.get(
            user_id=request.user) if DeliveryAddress.objects.filter(user_id=request.user).exists() else None
        payment.save()
        for cart in carts:
            if cart:
                item = Cart.objects.get(id=cart)
                amount += item.sub_total
                order = Order()
                order.phone_id = item.phone_id
                order.user_id = item.user_id
                order.quantity = item.quantity
                order.amount_charged = item.sub_total
                order.amount = item.sub_total
                order.discount = 0
                order.save()
                payment.orders.add(order)
        payment.amount = amount
        payment.carts = request.POST.get("carts")
        payment.save()
    url = f"/payment/{payment.id}"
    return redirect(url)


def selectGateway(request, pk):
    payment = Payment.objects.get(id=pk)
    context = {"payID": pk, "payment": payment}
    return render(request, "payments/gateway.html", context)


def sslCommerce(request, pk):
    payment = Payment.objects.get(id=pk)
    ssl_store = SSLCSession(sslc_is_sandbox=True, sslc_store_id='sabbi64edd5c46bbad',
                            sslc_store_pass='sabbi64edd5c46bbad@ssl')

    ssl_store.set_urls(success_url='http://127.0.0.1:8000/payment/ssl-commerce/callback/', fail_url='http://127.0.0.1:8000/payment/ssl-commerce/callback/',
                       cancel_url='http://127.0.0.1:8000/payment/ssl-commerce/callback/', ipn_url='http://127.0.0.1:8000/payment/ssl-commerce/callback/')

    amount = str(payment.amount)
    item_count = payment.orders.count()

    ssl_store.set_product_integration(total_amount=Decimal(amount), currency='BDT', product_category='Mobile',
                                      product_name='Phone', num_of_item=item_count, shipping_method='YES', product_profile='None')
    user = request.user

    ssl_store.set_customer_info(name=f"{user.first_name} {user.last_name}", email=f"{user.email}", address1='demo address',
                                address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')

    ssl_store.set_shipping_info(shipping_to='demo customer', address='demo address',
                                city='Dhaka', postcode='1209', country='Bangladesh')

    ssl_store.set_additional_values(
        value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d=f"{payment.id}")

    response_data = ssl_store.init_payment()
    payment.gateway = "SSL-Commerz"
    payment.save()

    url = response_data["GatewayPageURL"]
    return redirect(url)


@csrf_exempt
def sslCallback(request, pk):
    payment = Payment.objects.get(id=pk)
    context = {"payment": payment}
    return render(request, "payments/callback.html", context)


def stripeIntent(request, pk):
    payment = Payment.objects.get(id=pk)
    customer = stripe.Customer.create(
        email=request.user.email,
    )
    intent = stripe.PaymentIntent.create(
        description="SM Software services",
        amount=int(10 * 100),
        currency='USD',
        automatic_payment_methods={'enabled': True},
        customer=customer.id,
    )
    client_secret = intent.client_secret
    payment.payment_secret = client_secret
    payment.gateway = "Stripe"
    payment.save()
    context = {"intent": intent, "client_secret": client_secret}
    return render(request, "payments/stripe.html", context)


def stripe_callback(request):
    payment_intent = stripe.PaymentIntent.retrieve(
        request.GET.get("payment_intent"))
    payment = Payment.objects.get(
        payment_secret=payment_intent["client_secret"])
    if payment_intent["status"] == "succeeded":
        payment.is_paid = True
        payment.payment_status = "Success"
        payment.payment_id = payment_intent["id"]
        payment.save()
        for i in json.loads(payment.carts):
            if i:
                cart = Cart.objects.get(id=i)
                cart.delete()
    else:
        payment.payment_status = "Failed"
        payment.save()

    context = {"payment": payment}
    return render(request, "payments/callback.html", context)
