from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Enter a valid email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    email = models.EmailField(max_length=245, unique=True)
    first_name = models.CharField(max_length=245)
    last_name = models.CharField(max_length=245)
    gender = models.CharField(max_length=245, choices=genders)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.staff == True:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        if self.admin == True:
            return True
        else:
            return False


class Address(models.Model):
    country = models.CharField(max_length=245)
    state = models.CharField(max_length=245)
    city = models.CharField(max_length=245)
    street = models.CharField(max_length=245)
    postal = models.CharField(max_length=245)

    def __str__(self) -> str:
        return self.street


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=245)
    image = models.ImageField(upload_to="Profile", null=True, blank=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
