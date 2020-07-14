from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from data.transformers import RecipeTreeTransformer

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


class SessionCreateView(generic.CreateView):
    model = Session
    fields = "__all__"


class SessionUpdateView(generic.UpdateView):
    model = Session
    fields = "__all__"


class SessionDeleteView(generic.DeleteView):
    model = Session
    success_url = reverse_lazy("baking:session-list")
