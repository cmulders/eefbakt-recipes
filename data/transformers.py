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

    def __hash__(self):
        return hash((self.product, self.unit))

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False

        return self.unit == other.unit and self.product == other.product

    def __lt__(self, other):
        assert isinstance(other, Ingredient)
        return (self.product.name, self.amount,) < (other.product.name, other.amount,)

    def __add__(self, other):
        if other is None:
            return self

        assert self == other
        return Ingredient(
            amount=self.amount + other.amount, unit=self.unit, product=self.product
        )

    __radd__ = __add__


@dataclass
class Recipe:
    recipe: RecipeModel
    amount: int = 1
    valid: bool = True
    ingredients: List[Ingredient] = field(default_factory=list)
    base_recipes: List["Recipe"] = field(default_factory=list)

    def __iter__(self) -> Iterable["Recipe"]:
        yield self

        for r in self.base_recipes:
            yield from iter(r)

    def iter_ingredients(self) -> Iterable["Ingredient"]:
        for recipe in iter(self):
            yield from recipe.ingredients


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

    def transform(self, recipe: RecipeModel, scale: int = 1):
        self.visited = set()
        return self._transform_recipe(recipe, scale)
