from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('carts', views.Get_all_carts.as_view(), name="carts"),
    path('add-to-cart/<str:pk>/', views.AddToCarT.as_view(), name="add-to-cart"),
    path('remove-quantity/<str:pk>/',
         views.remove_quantity, name="remove-quantity"),
    path('remove-item/<str:pk>/',
         views.remove_from_cart, name="remove-cart"),
]
