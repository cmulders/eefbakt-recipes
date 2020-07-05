import operator

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["Product", "Ingredient", "Recipe"]


class Product(models.Model):
    class Unit(models.TextChoices):
        ML = "ml", _("milliliter")
        GR = "gr", _("gram")
        PIECE = "pcs", _("pieces")

    name = models.CharField(max_length=150)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.PIECE)

    ingredient = GenericRelation("Ingredient")

    def __str__(self):
        return _("Product: %(name)s") % {"name": self.name}


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe", related_name="ingredients", on_delete=models.CASCADE
    )

    limit = operator.or_(
        models.Q(app_label="data", model="product"),
        models.Q(app_label="data", model="recipe"),
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=limit
    )
    object_id = models.PositiveIntegerField()
    ingredient_object = GenericForeignKey()

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    ingredients: models.Model  # Reverse related field

    ingredient = GenericRelation(Ingredient)

    def __str__(self):
        return _("Recipe: %(name)s") % {"name": self.name}
