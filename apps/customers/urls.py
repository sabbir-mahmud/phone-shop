from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('settings', views.SettingsView.as_view(), name="settings"),
    path('orders', views.OrderView.as_view(), name="orders-status")
]
