from decimal import Decimal
from typing import *

from common.constants import Unit
from common.models import ImageTag, UnitConversion
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

__all__ = ["Product", "Recipe", "ProductIngredient", "RecipeIngredient"]


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
        "Product", on_delete=models.CASCADE, related_name="prices"
    )

    store = models.CharField(max_length=80, blank=True)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    @property
    def normalized_price(self) -> Decimal:
        return self.price / self.amount


class ProductIngredient(models.Model):

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    base_recipe = models.ForeignKey(
        "Recipe", on_delete=models.PROTECT, related_name="base_recipes"
    )

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class Recipe(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField("Product", through=ProductIngredient)
    productingredient_set: List[ProductIngredient]

    recipes = models.ManyToManyField(
        "Recipe", through=RecipeIngredient, through_fields=("recipe", "base_recipe",),
    )
    recipeingredient_set: List[RecipeIngredient]

    images = GenericRelation(ImageTag, related_name="+")

    def __str__(self):
        return self.name

    def __repr__(self):
        return _("Recipe: %(name)s") % {"name": self.name}

    def get_absolute_url(self):
        return reverse("data:recipe-detail", args=[self.pk])


class SessionProduct(models.Model):
    session = models.ForeignKey(
        "Session", related_name="ingredients", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class SessionRecipe(models.Model):
    session = models.ForeignKey(
        "Session", related_name="session_recipes", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class Session(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    recipe_description = models.TextField("Session recipe", blank=True)

    session_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipes = models.ManyToManyField(
        Recipe, through=SessionRecipe, related_name="sessions"
    )
    products = models.ManyToManyField(
        Product, through=SessionProduct, related_name="sessions"
    )

    images = GenericRelation(ImageTag, related_name="+")

    def __str__(self):
        return self.title

    def __repr__(self):
        return _("Session: %(title)s") % {"title": self.title}

    def get_absolute_url(self):
        return reverse("data:session-detail", args=[self.pk])

    class Meta:
        ordering = ["-session_date", "-updated_at"]
