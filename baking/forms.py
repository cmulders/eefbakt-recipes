from collections import deque

from django import forms
from django.utils.translation import gettext as _

from .models import Session, SessionProduct, SessionRecipe


class SessionRecipeForm(forms.ModelForm):
    class Meta:
        fields = [
            "recipe",
            "amount",
        ]

    def save(self, *args, **kwargs):
        self.instance.sort_key = self.cleaned_data.get("ORDER", 1) or 1

        return super().save(*args, **kwargs)


class SessionProductForm(forms.ModelForm):
    class Meta:
        fields = [
            "product",
            "amount",
            "unit",
        ]

    def save(self, *args, **kwargs):
        self.instance.sort_key = self.cleaned_data.get("ORDER", 1) or 1

        return super().save(*args, **kwargs)


class OrderFirstFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        if self.can_order:
            # Make the Ordering field the first,
            form.order_fields(["ORDER"])


SessionRecipeInlineFormset = forms.inlineformset_factory(
    Session,
    SessionRecipe,
    formset=OrderFirstFormSet,
    form=SessionRecipeForm,
    can_order=True,
    extra=1,
)

SessionProductInlineFormset = forms.inlineformset_factory(
    Session,
    SessionProduct,
    formset=OrderFirstFormSet,
    form=SessionProductForm,
    can_order=True,
    extra=1,
)
