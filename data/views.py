import functools
import itertools
import operator

from django.db.models.deletion import Collector, ProtectedError
from django.urls import reverse_lazy
from django.views import generic
from utils.views import DuplicateView, MixinObjectPageTitle, ModelFormWithInlinesView

from data.transformers import Recipe as RecipeViewModel
from data.transformers import RecipeTreeTransformer

from .constants import Unit
from .converters import UnitConverter
from .forms import (
    ImageTagInlineFormset,
    ProductIngredientInlineFormset,
    ProductPriceInlineFormset,
    RecipeIngredientInlineFormset,
    SessionProductInlineFormset,
    SessionRecipeInlineFormset,
    UnitConversionInlineFormset,
)
from .models import Product, Recipe, Session
from .transformers import RecipeTreeTransformer


class ProductListView(generic.ListView):
    model = Product

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET["q"])
        return qs


class ProductDetailView(MixinObjectPageTitle, generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        converter = UnitConverter(self.object.unit_conversions.all())
        kwargs.update(
            {
                "conversions": {
                    from_unit: [
                        (converter.scale(from_unit, to_unit), to_unit)
                        for to_unit in Unit
                    ]
                    for from_unit in Unit
                }
            }
        )
        return super().get_context_data(**kwargs)


class ProductFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
    model = Product
    fields = "__all__"
    inlines = {
        "prices": ProductPriceInlineFormset,
        "conversions": UnitConversionInlineFormset,
    }


class ProductCreateView(ProductFormsetFormView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class ProductUpdateView(ProductFormsetFormView):
    success_url = reverse_lazy("data:product-list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("data:product-list")

    def get_context_data(self, **kwargs):
        collector = Collector(using="default")
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)


class RecipeListView(generic.ListView):
    model = Recipe

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET["q"])
        return qs


class RecipeFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
    model = Recipe
    fields = ["name", "description"]

    inlines = {
        "products": ProductIngredientInlineFormset,
        "recipes": RecipeIngredientInlineFormset,
        "imagetags": ImageTagInlineFormset,
    }


class RecipeCreateView(RecipeFormsetFormView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class RecipeUpdateView(RecipeFormsetFormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class RecipeDeleteView(generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy("data:recipe-list")

    def get_context_data(self, **kwargs):
        collector = Collector(using="default")
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)


class RecipeDuplicateView(DuplicateView):
    model = Recipe


class RecipeDetailView(MixinObjectPageTitle, generic.DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        transformer = RecipeTreeTransformer()
        kwargs["transformed_object"] = transformer.transform(self.object)
        return super().get_context_data(**kwargs)


class SessionList(generic.ListView):
    model = Session

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(title__icontains=self.request.GET["q"])
        return qs


class SessionDetailView(MixinObjectPageTitle, generic.DetailView):
    model = Session

    def session_recipe_viewmodel(self):
        session = self.object
        transformer = RecipeTreeTransformer()

        return RecipeViewModel(
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

    def get_context_data(self, **kwargs):
        kwargs["session_recipe"] = self.session_recipe_viewmodel()
        return super().get_context_data(**kwargs)


class SessionExportView(SessionDetailView):
    template_name = "baking/session_export.html"


class SessionIngredientsDetailView(SessionDetailView):
    template_name = "baking/session_detail_ingredients.html"

    def get_context_data(self, **kwargs):
        session_recipe = self.session_recipe_viewmodel()
        ingredients = list(session_recipe.iter_ingredients())
        groups = itertools.groupby(sorted(ingredients))

        kwargs["ingredients"] = [functools.reduce(operator.add, g) for _, g in groups]
        kwargs["ingredients_total"] = sum(p.price or 0 for p in ingredients)
        return super().get_context_data(**kwargs)


class SessionFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
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


class SessionDuplicateView(DuplicateView):
    model = Session


class SessionDeleteView(generic.DeleteView):
    model = Session
    success_url = reverse_lazy("data:session-list")
