from typing import *

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from data.models import Product, Recipe


class SessionIngredients(models.Model):
    session = models.ForeignKey(
        "Session", related_name="ingredients", on_delete=models.CASCADE
    )
    source_recipe = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=150)
    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)


class SessionRecipe(models.Model):
    session = models.ForeignKey("Session", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=2)


class Session(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    session_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipes = models.ManyToManyField(
        Recipe, through=SessionRecipe, related_name="sessions"
    )
    ingredients: Union[models.QuerySet, List[SessionIngredients]]

    def __str__(self):
        return self.title

    def __repr__(self):
        return _("Session: %(title)s") % {"title": self.title}

    def get_absolute_url(self):
        return reverse("baking:session-detail", args=[self.pk])
