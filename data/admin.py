from functools import partial
from os import read

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.template.defaultfilters import filesizeformat, unordered_list
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    AlternateImageTag,
    ImageTag,
    Product,
    ProductIngredient,
    ProductPrice,
    Recipe,
    RecipeIngredient,
    Session,
    SessionProduct,
    SessionRecipe,
    UnitConversion,
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


def thumbnail(obj, width=500, height=500):
    return format_html(
        '<img src="{}" style="max-width: {}px; max-height:{}px; border-radius:5px" />',
        obj.image.url,
        int(width),
        int(height),
    )


thumbnail.__name__ = "Thumbnail"

tiny_thumbnail = partial(thumbnail, width=50, height=50)
tiny_thumbnail.__name__ = thumbnail.__name__

small_thumbnail = partial(thumbnail, width=150, height=150)
small_thumbnail.__name__ = thumbnail.__name__


def image_spec(obj):
    try:
        dims = f"{getattr(obj, 'width', '?')} × {getattr(obj, 'height', '?')}"
        size = filesizeformat(obj.image.size)
        return f"{dims} — {size}"
    except FileNotFoundError:
        return "(not found)"


# Register your models here.
class AlternateImageTagInline(admin.TabularInline):
    extra = 0
    model = AlternateImageTag

    fields = (
        tiny_thumbnail,
        image_spec,
        "image",
    )
    readonly_fields = (
        tiny_thumbnail,
        image_spec,
    )


@admin.register(ImageTag)
class ImageTagAdmin(admin.ModelAdmin):
    inlines = [AlternateImageTagInline]

    list_display = (
        "related_object",
        small_thumbnail,
        image_spec,
        "alternatives",
        "name",
    )
    list_display_links = (small_thumbnail, image_spec, "name")

    fields = (thumbnail, "image", image_spec, "name", "caption")
    readonly_fields = (thumbnail, image_spec)

    actions = ["make_thumbnails"]

    def related_object(self, obj):
        return str(obj.object)

    related_object.short_description = "Object"

    def alternatives(self, obj):
        return mark_safe(
            "<ul>"
            + unordered_list([image_spec(alt) for alt in obj.alternates.all()])
            + "</ul>"
        )

    def make_thumbnails(self, request, queryset):
        instance: ImageTag
        for instance in queryset.prefetch_related("alternates").all():
            instance.create_thumbnails()

    make_thumbnails.short_description = "Create thumbnails for selected images"


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    pass
