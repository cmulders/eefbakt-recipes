from collections import deque

from django import forms
from django.utils.translation import gettext as _

from .models import Product, ProductIngredient, Recipe, RecipeIngredient


class RecipeIngredientForm(forms.ModelForm):
    def clean_base_recipe(self):
        base_recipe = self.cleaned_data.get("base_recipe")

        to_visit = deque(r.base_recipe for r in base_recipe.recipeingredient_set.all())
        while to_visit:
            current = to_visit.pop()
            if current == base_recipe:
                raise forms.ValidationError(_("Recursive recipe detected"))

            to_visit.extendleft(
                r.base_recipe for r in current.recipeingredient_set.all()
            )

        return base_recipe

    class Meta:
        fields = "__all__"


class IngredientInlineFormset(forms.BaseInlineFormSet):
    pass


RecipeIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    formset=IngredientInlineFormset,
    fk_name="recipe",
)

ProductIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    ProductIngredient,
    formset=IngredientInlineFormset,
    fk_name="recipe",
    fields="__all__",
)
