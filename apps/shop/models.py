from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Wrapper(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(Wrapper):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Phone(Wrapper):
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    dp = models.ImageField(upload_to="shop/gallery",
                           default="shop/gallery/Apple-iPhone-8-Plus-Gold.jpg")
    model = models.CharField(max_length=50)
    colors = models.CharField(max_length=50)
    highlights = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.model


class Images(Wrapper):
    phone_id = models.ForeignKey(Phone, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="shop/gallery")

    def __str__(self) -> str:
        return str(self.img)


class Cart(Wrapper):
    phone_id = models.ForeignKey(Phone, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=100)

    def __str__(self) -> str:
        return str(self.id)


class Order(Wrapper):
    status = (('pending', 'pending'), ('shipped', 'shipped'),
              ('delivered', 'delivered'))
    phone_id = models.ForeignKey(Phone, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=100)
    delivery_status = models.CharField(
        max_length=30, null=True, blank=True, default="pending", choices=status)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        ordering = ('-id',)


class DeliveryAddress(Wrapper):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street_address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.user_id}"


class Payment(Wrapper):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    carts = models.CharField(max_length=100, blank=True, null=True, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gateway = models.CharField(max_length=50, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_secret = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    delivery = models.ForeignKey(
        DeliveryAddress, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}"
