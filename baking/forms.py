from collections import deque

from django import forms
from django.utils.translation import gettext as _

from .models import Session, SessionRecipe


class SessionRecipeForm(forms.ModelForm):
    class Meta:
        fields = "__all__"


SessionRecipeInlineFormset = forms.inlineformset_factory(
    Session, SessionRecipe, form=SessionRecipeForm,
)
