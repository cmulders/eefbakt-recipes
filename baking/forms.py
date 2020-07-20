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

        super().save(*args, **kwargs)


SessionRecipeInlineFormset = forms.inlineformset_factory(
    Session, SessionRecipe, form=SessionRecipeForm, can_order=True,
)
