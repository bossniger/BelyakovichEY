from django.db import models

from apps.shop.models import Product


class Country(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.PositiveIntegerField()


class Clients(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=60)
    amount_orders = models.IntegerField(null=True)
    orders_cost = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2
    )
    email = models.CharField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=14, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=90, blank=True)


# Create your models here.
