from django.urls import include, path
from django.views.generic import RedirectView

from . import views

app_name = "data"

# fmt: off
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="root"), name="index"),
    path("recipes/", include([
        path("", views.RecipeListView.as_view(), name="recipe-list"),
        path("new/", views.RecipeCreateView.as_view(), name="recipe-create"),
        path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
        path("<int:pk>/export/", views.RecipeExportView.as_view(), name="recipe-export"),
        path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="recipe-update"),
        path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
        path("<int:pk>/duplicate/", views.RecipeDuplicateView.as_view(), name="recipe-duplicate"),
    ])),
    path("products/", include([
        path("", views.ProductListView.as_view(), name="product-list"),
        path("new/", views.ProductCreateView.as_view(), name="product-create"),
        path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
        path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"),
        path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
    ])),
    path("sessions/", include([
        path("", views.SessionList.as_view(), name="session-list"),
        path("new/", views.SessionCreateView.as_view(), name="session-create"),
        path("<int:pk>/", views.SessionDetailView.as_view(), name="session-detail"),
        path("<int:pk>/ingredients/", views.SessionIngredientsDetailView.as_view(), name="session-ingredients"),
        path("<int:pk>/export/", views.SessionExportView.as_view(), name="session-export"),
        path("<int:pk>/edit/", views.SessionUpdateView.as_view(), name="session-update"),
        path("<int:pk>/duplicate/", views.SessionDuplicateView.as_view(), name="session-duplicate"),
        path("<int:pk>/delete/", views.SessionDeleteView.as_view(), name="session-delete"),
    ])),
]
