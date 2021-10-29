from typing import List

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .image import ImageTag
from .product import Product
from .unit import Unit


class ProductIngredient(models.Model):

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    base_recipe = models.ForeignKey(
        "Recipe", on_delete=models.PROTECT, related_name="base_recipes"
    )

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class Recipe(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.PIECE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(
        Product, through=ProductIngredient, related_name="recipes"
    )
    productingredient_set: List[ProductIngredient]

    recipes = models.ManyToManyField(
        "Recipe",
        through=RecipeIngredient,
        through_fields=(
            "recipe",
            "base_recipe",
        ),
    )
    recipeingredient_set: List[RecipeIngredient]

    images = GenericRelation(ImageTag, related_name="+")

    @property
    def title(self):
        base_str = self.name
        if self.amount is not None and self.unit:
            base_str += f" ({float(self.amount):g} {Unit(self.unit).short_name})"
        return base_str

    def __str__(self):
        return self.title

    def __repr__(self):
        return _("Recipe: %(name)s") % {"name": self.name}

    def get_absolute_url(self):
        return reverse("data:recipe-detail", args=[self.pk])
