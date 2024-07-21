from django.db import models
from users.models import User


class Bicycle(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="Название велосипеда")
    cost_per_minute = models.FloatField(null=False, blank=False, verbose_name="Стоимость аренды за минуту")
    user = models.ManyToManyField(User, verbose_name="Пользователь", blank=True, through="BicycleUser")


class BicycleUser(models.Model):
    bicycle = models.ForeignKey(Bicycle, null=False, blank=False, on_delete=models.PROTECT)
    user = models.ForeignKey(User, null=False, blank=True, on_delete=models.PROTECT)
    rent_start = models.DateTimeField(null=False, blank=False, auto_now_add=True)
