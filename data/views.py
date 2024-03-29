import functools
import itertools
import operator
from urllib.parse import urlencode

from django.db.models.deletion import Collector, ProtectedError
from django.urls import NoReverseMatch, reverse_lazy
from django.urls.base import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from django.views.generic.list import MultipleObjectMixin
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


class ElidedPaginatorContextMixin(MultipleObjectMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get("paginator", False):
            paginator = context["paginator"]
            page_obj = context["page_obj"]
            elided_range = paginator.get_elided_page_range(page_obj.number)
            context["elided_page_range"] = elided_range
            if hasattr(self, "request"):
                context["query"] = urlencode(
                    {"q": getattr(self, "request").GET.get("q", "")}
                )
        return context


class ProductListView(ElidedPaginatorContextMixin, ListView):
    model = Product
    paginate_by = 250

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET["q"])
        return qs


class ProductDetailView(MixinObjectPageTitle, DetailView):
    model = Product

    def get_related_recipes(self):
        return self.object.recipes.order_by("-updated_at").all()

    def get_related_sessions(self):
        return self.object.sessions.order_by("-session_date").all()

    def get_context_data(self, **kwargs):
        converter = UnitConverter(self.object.unit_conversions.all())
        kwargs.update({"conversions": converter.conversion_matrix})
        kwargs["related_recipes"] = self.get_related_recipes()
        kwargs["related_sessions"] = self.get_related_sessions()
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


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("data:product-list")

    def get_context_data(self, **kwargs):
        qs = self.get_queryset()
        collector = Collector(using=qs.db)
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)


class RecipeListView(ElidedPaginatorContextMixin, ListView):
    model = Recipe
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET["q"])
        return qs


class RecipeFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
    model = Recipe
    fields = ["name", "description", "amount", "unit"]

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
    def get_success_url(self) -> str:
        refid = self.request.POST.get("refid", None)
        ref = self.request.POST.get("ref", None)

        if ref and refid:
            try:
                return reverse(ref, args=[refid])
            except NoReverseMatch:
                pass  # just use the regular success url

        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy("data:recipe-list")

    def get_context_data(self, **kwargs):
        qs = self.get_queryset()
        collector = Collector(using=qs.db)
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)


class RecipeDuplicateView(DuplicateView):
    model = Recipe


class RecipeDetailView(MixinObjectPageTitle, DetailView):
    model = Recipe

    def get_related_sessions(self):
        return self.object.sessions.order_by("-session_date").all()

    def get_transformed_object(self):
        transformer = RecipeTreeTransformer()
        return transformer.transform(self.object)

    def get_context_data(self, **kwargs):
        kwargs["transformed_object"] = self.get_transformed_object()
        kwargs["related_sessions"] = self.get_related_sessions()
        return super().get_context_data(**kwargs)


class RecipeExportView(RecipeDetailView):
    template_name = "data/recipe_export.html"

    def get_related_sessions(self):
        # Hide related on export
        return []


class SessionList(ElidedPaginatorContextMixin, ListView):
    model = Session
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
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


class SessionExportView(SessionDetailView):
    template_name = "data/session_export.html"


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
