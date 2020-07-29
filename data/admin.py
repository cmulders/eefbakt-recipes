from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.models import ContentType

from .models import ImageTag, Product, ProductIngredient, Recipe, RecipeIngredient


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fk_name = "recipe"


class ImageTagInline(GenericStackedInline):
    model = ImageTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline, RecipeIngredientInline, ImageTagInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
