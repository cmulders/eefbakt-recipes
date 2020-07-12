from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "data"

# fmt: off
urlpatterns = [
    path("", TemplateView.as_view(template_name='data/index.html'), name="data-index"),
    path("recipes/", views.RecipeListView.as_view(), name="recipe-list"),
    path("recipes/new/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path("recipes/<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="recipe-update"),
    path("recipes/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
    path("recipes/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/new/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
]
