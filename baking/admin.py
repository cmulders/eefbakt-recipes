from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import ImageTag, Session, SessionProduct, SessionRecipe


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
