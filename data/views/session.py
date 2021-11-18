import functools
import itertools
import operator

from data.transformers import Recipe as RecipeViewModel
from data.transformers import RecipeTreeTransformer
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from utils.views import DuplicateView, MixinObjectPageTitle, ModelFormWithInlinesView

from ..forms import (
    ImageTagInlineFormset,
    SessionProductInlineFormset,
    SessionRecipeInlineFormset,
)
from ..models import Session
from ..transformers import RecipeTreeTransformer
from .common import RecipeKindNamespaceMixin

__all__ = [
    "SessionList",
    "SessionDetailView",
    "SessionIngredientsDetailView",
    "SessionCreateView",
    "SessionUpdateView",
    "SessionDeleteView",
    "SessionDuplicateView",
    "SessionExportView",
]


class SessionList(RecipeKindNamespaceMixin, ListView):
    model = Session

    def get_queryset(self):
        qs = super().get_queryset()  # type: ignore
        qs = qs.filter(kind__in=self.recipe_kinds)

        if "q" in self.request.GET:
            qs = qs.filter(title__icontains=self.request.GET["q"])
        return qs


class SessionDetailView(MixinObjectPageTitle, DetailView):
    model = Session

    def session_recipe_viewmodel(self):
        session = self.object
        transformer = RecipeTreeTransformer()

        return RecipeViewModel(
            ingredients=[
                transformer.transform_product(product)
                for product in (session.ingredients.select_related("product").all())
            ],
            base_recipes=[
                transformer.transform_recipe(r.recipe, scale=r.amount)
                for r in session.session_recipes.select_related("recipe").all()
            ],
        )

    def get_context_data(self, **kwargs):
        kwargs["session_recipe"] = self.session_recipe_viewmodel()
        return super().get_context_data(**kwargs)


class SessionIngredientsDetailView(SessionDetailView):
    template_name = "data/session_detail_ingredients.html"

    def get_context_data(self, **kwargs):
        session_recipe = self.session_recipe_viewmodel()
        ingredients = sorted(session_recipe.iter_ingredients())
        groups = itertools.groupby(ingredients)

        kwargs["ingredients"] = [functools.reduce(operator.add, g) for _, g in groups]
        kwargs["ingredients_total"] = sum(p.price for p in ingredients if p.price)
        return super().get_context_data(**kwargs)


class SessionFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
    model = Session
    fields = [
        "title",
        "description",
        "recipe_description",
        "session_date",
        "kind",
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


class SessionDuplicateView(DuplicateView):
    model = Session


class SessionDeleteView(DeleteView):
    model = Session
    success_url = reverse_lazy("data:session-list")


class SessionExportView(SessionDetailView):
    template_name = "data/session_export.html"
