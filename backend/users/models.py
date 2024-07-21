from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractBaseUser):
    name = models.CharField(max_length=254, null=False, blank=False, verbose_name="Имя")
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name="Электронная почта")

    objects = UserManager()

    USERNAME_FIELD = "email"


class UserBill(models.Model):
    user = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE, null=False, blank=False)
    bill = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    duration = models.IntegerField(null=False, blank=False)
