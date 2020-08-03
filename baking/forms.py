from collections import deque

from django import forms
from django.utils.translation import gettext as _

from utils.fields import CreatingModelChoiceField
from utils.forms import OrderdedModelForm
from utils.formsets import OrderFirstInlineFormSet

from .models import Session, SessionProduct, SessionRecipe


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


SessionRecipeInlineFormset = forms.inlineformset_factory(
    Session,
    SessionRecipe,
    formset=OrderFirstInlineFormSet,
    form=OrderdedModelForm,
    fields=["recipe", "amount",],
    can_order=True,
    extra=3,
)

SessionProductInlineFormset = forms.inlineformset_factory(
    Session,
    SessionProduct,
    formset=OrderFirstInlineFormSet,
    form=OrderdedModelForm,
    formfield_callback=product_formfield_callback,
    fields=["product", "amount", "unit",],
    can_order=True,
    extra=3,
)
