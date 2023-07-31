from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('add-to-cart/<str:pk>/', views.AddToCarT.as_view(), name="add-to-cart")
]
