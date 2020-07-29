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
from data.transformers import Ingredient, RecipeTreeTransformer

from .forms import SessionProductInlineFormset, SessionRecipeInlineFormset
from .models import Session


class SessionList(generic.ListView):
    model = Session


class SessionDetailView(generic.DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        transformer = RecipeTreeTransformer()
        kwargs["ingredient_view_objects"] = [
            Ingredient(
                amount=product.amount, unit=product.unit, product=product.product,
            )
            for product in (self.object.ingredients.select_related("product").all())
        ]
        kwargs["recipe_view_objects"] = [
            transformer.transform(r.recipe, r.amount)
            for r in self.object.session_recipes.select_related("recipe").all()
        ]
        return super().get_context_data(**kwargs)


class SessionIngredientsDetailView(generic.DetailView):
    model = Session
    template_name = "baking/session_detail_ingredients.html"

    def get_context_data(self, **kwargs):
        transformer = RecipeTreeTransformer()
        ingredients = [
            ingredient
            for session_recipe in self.object.session_recipes.all()
            for ingredient in transformer.transform(
                session_recipe.recipe, session_recipe.amount
            ).iter_ingredients()
        ]
        ingredients.extend(
            Ingredient(
                amount=product.amount, unit=product.unit, product=product.product,
            )
            for product in (self.object.ingredients.select_related("product").all())
        )
        groups = itertools.groupby(
            sorted(ingredients), key=lambda x: (x.unit, x.product,)
        )

        kwargs["ingredients"] = [functools.reduce(operator.add, g) for _, g in groups]
        return super().get_context_data(**kwargs)


class SessionFormsetFormView(
    edit.SingleObjectTemplateResponseMixin, edit.ModelFormMixin, edit.ProcessFormView
):
    model = Session
    fields = [
        "title",
        "description",
        "session_date",
    ]
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
                prefix="products", cls=SessionProductInlineFormset
            ),
            "recipes_formset": self.get_inline(
                prefix="recipes", cls=SessionRecipeInlineFormset
            ),
            "imagetags_formset": self.get_inline(
                prefix="images", cls=ImageTagInlineFormset
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
