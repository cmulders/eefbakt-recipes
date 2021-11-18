from typing import Callable, List

from data.constants import RecipeKind
from django.views import View


class RecipeKindNamespaceMixin(View):
    @property
    def recipe_kinds(self) -> List[RecipeKind]:
        try:
            return [RecipeKind(self.request.resolver_match.namespace)]
        except ValueError:
            return list(RecipeKind)
