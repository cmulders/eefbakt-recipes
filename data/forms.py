from collections import deque

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count
from django.utils.translation import gettext as _

from utils.fields import CreatingModelChoiceField
from utils.forms import OrderdedModelForm
from utils.formsets import OrderFirstInlineFormSet

from .models import Product, ProductIngredient, ProductPrice, Recipe, RecipeIngredient


class RecipeIngredientForm(OrderdedModelForm):
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


def product_formfield_callback(f, **kwargs):
    if f.name == "product":
        kwargs.update(
            {
                "form_class": CreatingModelChoiceField,
                "creation_field": "name",
                "widget": forms.Select(attrs={"data-tags": "true"}),
                "queryset": Product.objects.annotate(
                    use_count=Count("sessionproduct")
                    + Count("productingredient")
                    + Count("sessions")
                ).order_by("-use_count", "name"),
            }
        )
    return f.formfield(**kwargs)


RecipeIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    formset=OrderFirstInlineFormSet,
    fields=["base_recipe", "amount"],
    fk_name="recipe",
    can_order=True,
    extra=3,
)

ProductIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    ProductIngredient,
    form=OrderdedModelForm,
    formset=OrderFirstInlineFormSet,
    fk_name="recipe",
    fields=["product", "amount", "unit"],
    can_order=True,
    extra=3,
    formfield_callback=product_formfield_callback,
)

ProductPriceInlineFormset = forms.inlineformset_factory(
    Product, ProductPrice, fields="__all__"
)
