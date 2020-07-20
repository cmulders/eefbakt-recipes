import functools
import itertools
import operator

from crispy_forms.helper import FormHelper
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit

from .forms import SessionRecipeInlineFormset
from .models import Session


class SessionList(generic.ListView):
    model = Session


class SessionDetailView(generic.DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        transformer = RecipeTreeTransformer()
        kwargs["recipe_view_objects"] = [
            transformer.transform(r) for r in self.object.recipes.all()
        ]
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

    def get_recipe_formset(self):
        kwargs = {
            "prefix": "recipes",
            "instance": self.object,
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {"data": self.request.POST, "files": self.request.FILES,}
            )

        return SessionRecipeInlineFormset(**kwargs)

    def get_formset_helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.form_id = "recipe-inline-formset"
        helper.template = "bootstrap4/table_inline_formset.html"
        return helper

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "formset_helper": self.get_formset_helper(),
                "recipes_formset": self.get_recipe_formset(),
            }
        )
        return super().get_context_data(**kwargs)

    def form_valid(self, form, recipes_formset):
        response = super().form_valid(form)

        recipes_formset.instance = self.object
        recipes_formset.save()
        return response

    def form_invalid(self, form, recipes_formset):
        """If the form is invalid, render the invalid form and formsets."""
        return self.render_to_response(
            self.get_context_data(form=form, recipes_formset=recipes_formset,)
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate the form and formset instances with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        recipes_formset = self.get_recipe_formset()
        if form.is_valid() and recipes_formset.is_valid():
            return self.form_valid(form, recipes_formset)
        else:
            return self.form_invalid(form, recipes_formset)


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
