from .models import Cart


def carts(request):
    count = 0
    if Cart.objects.all().exists():
        count = Cart.objects.filter(user_id=request.user).count()
    return {"count": count}
