from decimal import Decimal
from typing import List

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .unit import Unit, UnitConversion


class Product(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=150, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prices: List["ProductPrice"]

    unit_conversions = GenericRelation(UnitConversion, related_name="+")

    def get_absolute_url(self):
        return reverse("data:product-detail", args=[self.pk])

    def __str__(self):
        return self.name

    def __repr__(self):
        return _("Product: %(name)s") % {"name": self.name}


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )

    store = models.CharField(max_length=80, blank=True)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    @property
    def normalized_price(self) -> Decimal:
        return self.price / self.amount
