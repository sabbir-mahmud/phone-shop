from django.db.models.signals import post_save

from .models import Cart


def cart_handler(sender, instance, created, *args, **kwargs):
    if created:
        print(instance.phone_id.discount_price)
        instance.sub_total = instance.phone_id.discount_price * instance.quantity
        instance.save()


post_save.connect(cart_handler, sender=Cart)
