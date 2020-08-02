from collections import deque

from django import forms
from django.core.exceptions import ImproperlyConfigured
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


class CreatingModelChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, *args, creation_field=None, **kwargs):
        opts = queryset.model._meta
        model_field_names = [f.name for f in opts.get_fields()]

        if not creation_field:
            raise ImproperlyConfigured(
                f"'creation_field' should not be empty, but one of {', '.join(model_field_names)}"
            )
        if not creation_field in model_field_names:
            raise ImproperlyConfigured(
                f"'{creation_field}' should be one of {','.join(model_field_names)}"
            )

        self.creation_field = creation_field

    def to_python(self, value):
        try:
            return super().to_python(value)
        except forms.ValidationError as err:
            if err.code != "invalid_choice":
                raise  # Reraise the Validation error, only invalid choice we handle

        # Create a new model on the fly
        return self.queryset.model.objects.create(**{self.creation_field: value})


def product_formfield_callback(f, **kwargs):
    if f.name == "product":
        kwargs.update(
            {
                "form_class": CreatingModelChoiceField,
                "creation_field": "name",
                "widget": forms.Select(attrs={"data-tags": "true"}),
            }
        )
    return f.formfield(**kwargs)


RecipeIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    fields="__all__",
    fk_name="recipe",
    extra=1,
)

ProductIngredientInlineFormset = forms.inlineformset_factory(
    Recipe,
    ProductIngredient,
    fk_name="recipe",
    fields="__all__",
    extra=1,
    formfield_callback=product_formfield_callback,
)
