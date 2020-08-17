from typing import *

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.constants import Unit
from common.models import ImageTag
from data.models import Product, Recipe


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
        return reverse("baking:session-detail", args=[self.pk])

    class Meta:
        ordering = ["-session_date", "-updated_at"]
