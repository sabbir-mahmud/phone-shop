from django.contrib import admin

from .models import Brand, Cart, Images, Order, Payment, Phone

admin.site.register(Brand)
admin.site.register(Phone)
admin.site.register(Images)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Payment)
