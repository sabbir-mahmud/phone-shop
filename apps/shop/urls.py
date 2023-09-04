from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('carts', views.Get_all_carts.as_view(), name="carts"),
    path('add-to-cart/<str:pk>/', views.AddToCarT.as_view(), name="add-to-cart"),
    path('remove-quantity/<str:pk>/',
         views.remove_quantity, name="remove-quantity"),
    path('remove-item/<str:pk>/',
         views.remove_from_cart, name="remove-cart"),
    path('generate-payment', views.generatePayment, name="generate-payment"),
    path('payment/<str:pk>/', views.selectGateway, name="select-gateway"),
    path('payment/ssl-commerce/<str:pk>/', views.sslCommerce, name="ssl-com"),
    path('payment/ssl-commerce/callback/<str:pk>/',
         csrf_exempt(views.sslCallback), name="ssl-callback"),
    path('payment/stripe/<str:pk>/', views.stripeIntent, name="stripe-intent"),
    path("payment/stripe/callback", views.stripe_callback, name="stripe-callback")
]
