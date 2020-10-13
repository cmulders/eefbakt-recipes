from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import (
    ImageTag,
    Product,
    ProductIngredient,
    ProductPrice,
    Recipe,
    RecipeIngredient,
    Session,
    SessionProduct,
    SessionRecipe,
)


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fk_name = "recipe"


class ImageTagInline(GenericStackedInline):
    model = ImageTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline, RecipeIngredientInline, ImageTagInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPriceInline]
    readonly_fields = ["created_at", "updated_at"]


class SessionProductInline(admin.TabularInline):
    model = SessionProduct


class SessionRecipeInline(admin.TabularInline):
    model = SessionRecipe


class ImageTagInline(GenericStackedInline):
    model = ImageTag


@admin.register(Session)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [SessionProductInline, SessionRecipeInline, ImageTagInline]
    readonly_fields = ["created_at", "updated_at"]
