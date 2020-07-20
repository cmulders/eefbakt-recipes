from collections import deque

from django import forms
from django.utils.translation import gettext as _

from .models import Session, SessionRecipe


class SessionRecipeForm(forms.ModelForm):
    class Meta:
        fields = [
            "recipe",
            "amount",
        ]

    def save(self, *args, **kwargs):
        self.instance.sort_key = self.cleaned_data.get("ORDER", 1) or 1

        return super().save(*args, **kwargs)


class SessionRecipeFormSet(forms.BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)

        # Make the Ordering field the first, 
        form.order_fields(["ORDER"])
        return form


SessionRecipeInlineFormset = forms.inlineformset_factory(
    Session,
    SessionRecipe,
    formset=SessionRecipeFormSet,
    form=SessionRecipeForm,
    can_order=True,
)
