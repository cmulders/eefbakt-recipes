from typing import *

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

__all__ = ["Product", "Recipe", "ProductIngredient", "RecipeIngredient"]


class Product(models.Model):
    name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("data:product-detail", args=[self.pk])

    def __str__(self):
        return self.name

    def __repr__(self):
        return _("Product: %(name)s") % {"name": self.name}


class ProductIngredient(models.Model):
    class Unit(models.TextChoices):
        ML = "mL", _("milliliter")
        GR = "g", _("gram")
        PIECE = "pcs", _("pieces")

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.PIECE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    base_recipe = models.ForeignKey(
        "Recipe", on_delete=models.PROTECT, related_name="base_recipes"
    )

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)


class Recipe(models.Model):
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return _("Recipe: %(name)s") % {"name": self.name}

    def get_absolute_url(self):
        return reverse("data:recipe-detail", args=[self.pk])
