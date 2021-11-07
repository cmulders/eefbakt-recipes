from data import models, views
from data.constants import RecipeKind
from data.views.recipe import RecipeCreateView
from django.urls import include, path
from django.views.generic import RedirectView

app_name = "sweet_bread"

recipe_qs = models.Recipe.objects.for_kinds(RecipeKind.SWEET, RecipeKind.BREAD)
session_qs = models.Session.objects.for_kinds(RecipeKind.SWEET, RecipeKind.BREAD)

# fmt: off
urlpatterns = [
    path("recipes/", include([
        path("", views.RecipeListView.as_view(queryset=recipe_qs), name="recipe-list"),
    ])),
    path("sessions/", include([
        path("", views.SessionList.as_view(queryset=session_qs), name="session-list"),
    ])),
]
