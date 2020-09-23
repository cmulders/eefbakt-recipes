import functools
import itertools
import operator

from crispy_forms.helper import FormHelper
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit

from common.forms import ImageTagInlineFormset
from data.transformers import Ingredient, Recipe, RecipeTreeTransformer
from utils.views import ModelFormWithInlinesView

from .forms import SessionProductInlineFormset, SessionRecipeInlineFormset
from .models import Session


def create_session_recipe(session: Session):
    transformer = RecipeTreeTransformer()

    return Recipe(
        recipe=None,
        ingredients=[
            transformer.transform_product(product)
            for product in (session.ingredients.select_related("product").all())
        ],
        base_recipes=[
            transformer.transform_recipe(r.recipe, scale=r.amount)
            for r in session.session_recipes.select_related("recipe").all()
        ],
    )


class SessionList(generic.ListView):
    model = Session


class SessionDetailView(generic.DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        kwargs["session_recipe"] = create_session_recipe(self.object)
        return super().get_context_data(**kwargs)


class SessionIngredientsDetailView(generic.DetailView):
    model = Session
    template_name = "baking/session_detail_ingredients.html"

    def get_context_data(self, **kwargs):
        session_recipe = create_session_recipe(self.object)
        ingredients = list(session_recipe.iter_ingredients())
        groups = itertools.groupby(sorted(ingredients))

        kwargs["ingredients"] = [functools.reduce(operator.add, g) for _, g in groups]
        kwargs["ingredients_total"] = sum(p.price or 0 for p in ingredients)
        return super().get_context_data(**kwargs)


class SessionFormsetFormView(ModelFormWithInlinesView):
    model = Session
    fields = [
        "title",
        "description",
        "recipe_description",
        "session_date",
    ]
    inlines = {
        "products": SessionProductInlineFormset,
        "recipes": SessionRecipeInlineFormset,
        "images": ImageTagInlineFormset,
    }


class SessionCreateView(SessionFormsetFormView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class SessionUpdateView(SessionFormsetFormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class SessionDeleteView(generic.DeleteView):
    model = Session
    success_url = reverse_lazy("baking:session-list")
