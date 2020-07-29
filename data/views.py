from crispy_forms.helper import FormHelper
from django.db import transaction
from django.db.models.deletion import Collector, ProtectedError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit

from .forms import ProductIngredientInlineFormset, RecipeIngredientInlineFormset
from .models import Product, Recipe
from .transformers import RecipeTreeTransformer

# Create your views here.


class ProductListView(generic.ListView):
    model = Product


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(generic.CreateView):
    model = Product
    fields = "__all__"


class ProductUpdateView(generic.UpdateView):
    model = Product
    fields = "__all__"


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


class RecipeFormsetFormView(
    edit.SingleObjectTemplateResponseMixin, edit.ModelFormMixin, edit.ProcessFormView
):
    model = Recipe
    fields = ["name", "description"]
    template_name_suffix = "_form"

    def get_inline(self, prefix, cls):
        kwargs = {
            "prefix": prefix,
            "instance": self.object,
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )

        return cls(**kwargs)

    def get_inlines(self):
        return {
            "products_formset": self.get_inline(
                prefix="products", cls=ProductIngredientInlineFormset
            ),
            "recipes_formset": self.get_inline(
                prefix="recipes", cls=RecipeIngredientInlineFormset
            ),
        }

    def get_formset_helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.use_custom_control = False
        helper.template = "bootstrap4/table_inline_formset.html"
        return helper

    def get_context_data(self, **kwargs):
        kwargs.update(
            {"formset_helper": self.get_formset_helper(), "inlines": self.get_inlines()}
        )
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form, inlines={}):
        response = super().form_valid(form)

        for inline in inlines.values():
            inline.instance = self.object
            inline.save()

        return response

    def form_invalid(self, form, inlines={}):
        """If the form is invalid, render the invalid form and formsets."""
        return self.render_to_response(self.get_context_data(form=form, **inlines,))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate the form and formset instances with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        inlines = self.get_inlines()
        if form.is_valid() and all(inline.is_valid() for inline in inlines.values()):
            return self.form_valid(form, inlines)
        else:
            return self.form_invalid(form, inlines)


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


class RecipeDetailView(generic.DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        transformer = RecipeTreeTransformer()
        kwargs["transformed_object"] = transformer.transform(self.object)
        return super().get_context_data(**kwargs)
