from collections import defaultdict
from dataclasses import dataclass, field
from typing import *

from .models import Product, ProductIngredient
from .models import Recipe as RecipeModel


@dataclass(frozen=True)
class Ingredient:
    amount: int
    unit: str
    product: Product


@dataclass
class Recipe:
    recipe: RecipeModel
    amount: int = 1
    valid: bool = True
    ingredients: List[Ingredient] = field(default_factory=list)
    base_recipes: List["Recipe"] = field(default_factory=list)

    def flatten_recipes(self, yield_self=True) -> Iterable["Recipe"]:
        if yield_self:
            yield self.recipe

        for r in self.base_recipes:
            yield r.recipe
            yield from r.flatten_recipes(yield_self=False)


class RecipeTreeTransformer:
    def _transform_product(
        self, ingredient: ProductIngredient, scale: int = 1
    ) -> Ingredient:
        return Ingredient(
            amount=ingredient.amount * scale,
            unit=ingredient.unit,
            product=ingredient.product,
        )

    def _transform_recipe(self, recipe: RecipeModel, scale: int = 1) -> Recipe:
        if recipe in self.visited:
            return Recipe(recipe=recipe, valid=False)
        self.visited.add(recipe)

        return Recipe(
            amount=scale,
            recipe=recipe,
            ingredients=[
                self._transform_product(p, scale=scale)
                for p in recipe.productingredient_set.all()
            ],
            base_recipes=[
                self._transform_recipe(r.base_recipe, scale=scale * r.amount)
                for r in recipe.recipeingredient_set.all()
            ],
        )

    def transform(self, recipe: RecipeModel):
        self.visited = set()
        return self._transform_recipe(recipe)
