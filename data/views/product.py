from django.db.models.deletion import Collector, ProtectedError
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from utils.views import MixinObjectPageTitle, ModelFormWithInlinesView

from ..converters import UnitConverter
from ..forms import ProductPriceInlineFormset, UnitConversionInlineFormset
from ..models import Product

__all__ = [
    "ProductListView",
    "ProductDetailView",
    "ProductFormsetFormView",
    "ProductCreateView",
    "ProductUpdateView",
    "ProductDeleteView",
]


class ProductListView(ListView):
    model = Product

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
        collector = Collector(using=self.queryset.db)
        try:
            collector.collect([self.object])
        except ProtectedError as err:
            kwargs.update({"protected_by": err.protected_objects})
        return super().get_context_data(**kwargs)
