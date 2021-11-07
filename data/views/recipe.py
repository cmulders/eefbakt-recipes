from data.transformers import RecipeTreeTransformer
from django.db.models.deletion import Collector, ProtectedError
from django.urls import NoReverseMatch, reverse_lazy
from django.urls.base import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from utils.views import DuplicateView, MixinObjectPageTitle, ModelFormWithInlinesView

from ..forms import (
    ImageTagInlineFormset,
    ProductIngredientInlineFormset,
    RecipeIngredientInlineFormset,
)
from ..models import Recipe
from ..transformers import RecipeTreeTransformer

__all__ = [
    "RecipeListView",
    "RecipeDetailView",
    "RecipeCreateView",
    "RecipeUpdateView",
    "RecipeDeleteView",
    "RecipeDuplicateView",
    "RecipeExportView",
]


class RecipeListView(ListView):
    model = Recipe

    def get_queryset(self):
        qs = super().get_queryset()
        if "q" in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET["q"])
        return qs


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


class RecipeFormsetFormView(MixinObjectPageTitle, ModelFormWithInlinesView):
    model = Recipe
    fields = [
        "name",
        "description",
        "amount",
        "unit",
        "kind",
    ]

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
        collector = Collector(using=self.queryset.db)
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)


class RecipeDuplicateView(DuplicateView):
    model = Recipe


class RecipeExportView(RecipeDetailView):
    template_name = "data/recipe_export.html"

    def get_related_sessions(self):
        # Hide related on export
        return []
