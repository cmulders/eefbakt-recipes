from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "baking"

# fmt: off
urlpatterns = [
    #path("", TemplateView.as_view(template_name='data/index.html'), name="session-index"),
    path("sessions/", views.SessionList.as_view(), name="session-list"),
    path("sessions/new/", views.SessionCreateView.as_view(), name="session-create"),
    path("sessions/<int:pk>/", views.SessionDetailView.as_view(), name="session-detail"),
    path("sessions/<int:pk>/ingredients/", views.SessionIngredientsDetailView.as_view(), name="session-ingredients"),
    path("sessions/<int:pk>/edit/", views.SessionUpdateView.as_view(), name="session-update"),
    path("sessions/<int:pk>/duplicate/", views.SessionDuplicateView.as_view(), name="session-duplicate"),
    path("sessions/<int:pk>/delete/", views.SessionDeleteView.as_view(), name="session-delete"),
]
