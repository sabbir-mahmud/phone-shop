import django.urls
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from sslcommerz_lib import SSLCOMMERZ

from apps.shop.models import Cart, Payment


class SSLCSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if "HTTP_ORIGIN" in request.META and request.path == "/payment/ssl-commerce/callback/":
            print('running ssl')
            print('line 17', request.path)
            if request.META["HTTP_ORIGIN"] != 'null':
                pass
            else:
                if request.method == "POST" or request.method == "post":
                    settings = {'store_id': 'sabbi64edd5c46bbad',
                                'store_pass': 'sabbi64edd5c46bbad@ssl', 'issandbox': True}
                    payment = SSLCOMMERZ(settings)
                    pay_id = request.POST.get("tran_id")
                    status = payment.transaction_query_tranid(pay_id)

                    if status['element'][0]["status"] == "VALID":
                        payment = Payment.objects.get(
                            id=status['element'][0]["value_d"])
                        payment.payment_id = pay_id
                        payment.is_paid = True
                        payment.payment_status = "Success"
                        payment.save()

                        for i in payment.carts.split(","):
                            if i:
                                cart = Cart.objects.get(id=i)
                                cart.delete()
                        url = f"/payment/ssl-commerce/callback/{payment.id}/"
                        return redirect(url)
                    else:
                        payment = Payment.objects.get(
                            id=status['element'][0]["value_d"])
                        payment.payment_status = "failed"
                        payment.save()
                        url = f"/payment/ssl-commerce/callback/{payment.id}/"
                        return redirect(url)

        response = self.get_response(request)
        return response


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
