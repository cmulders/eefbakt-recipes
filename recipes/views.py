from django.views import generic

from baking.models import Session
from data.models import Product, Recipe


class IndexView(generic.TemplateView):
    template_name = "home.html"

    def get_last_products(self):
        return Product.objects.order_by("-updated_at").all()[:5]

    def get_last_recipes(self):
        return Recipe.objects.order_by("-updated_at").all()[:5]

    def get_last_sessions(self):
        return Session.objects.order_by("-updated_at").all()[:5]

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "last_products": self.get_last_products(),
                "last_recipes": self.get_last_recipes(),
                "last_sessions": self.get_last_sessions(),
            }
        )

        return super().get_context_data(**kwargs)
