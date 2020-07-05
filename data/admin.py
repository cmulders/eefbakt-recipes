from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Ingredient, Product, Recipe


class IngredientModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the generic ModelChoiceField
        opts = self._meta
        model = opts.model
        ct_field = model._meta.get_field("content_type")
        fk_field = model._meta.get_field("object_id")

        print(ct_field.)
        print(ct_field, fk_field)
        self.fields["ingredient"] = forms.ChoiceField(choices=())

    def validate_ingredient(self, value):
        raise Exception(value)

    class Meta:
        model = Ingredient
        exclude = ["content_type", "object_id"]


class IngredientInline(admin.TabularInline):
    form = IngredientModelForm
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
