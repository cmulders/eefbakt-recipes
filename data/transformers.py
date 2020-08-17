from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import *

from common.constants import Unit
from common.converters import UnitConverter
from data.models import Product, ProductIngredient
from data.models import Recipe as RecipeModel


@dataclass(frozen=True)
class Ingredient:
    amount: int
    unit: Unit
    product: Product

    def __hash__(self):
        return hash((self.product, self.unit))

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False

        return self.unit == other.unit and self.product == other.product

    def __lt__(self, other):
        assert isinstance(other, Ingredient)
        return (self.product.name, self.unit, self.amount,) < (
            other.product.name,
            other.unit,
            other.amount,
        )

    def __add__(self, other):
        if other is None:
            return self

        assert self == other
        return Ingredient(
            amount=self.amount + other.amount, unit=self.unit, product=self.product
        )

    __radd__ = __add__

    @cached_property
    def unit_converter(self):
        return UnitConverter(self.product.unit_conversions.all())

    @property
    def price(self):
        if not self.product or not self.product.prices.all():
            return None

        prices = [
            price
            for price in self.product.prices.all()
            if Unit(price.unit) == self.unit
            or self.unit_converter.has_conversion(price.unit, self.unit)
        ]

        if not prices:
            return None

        return min(
            float(price.normalized_price * self.amount)
            * self.unit_converter.scale(self.unit, price.unit)
            for price in prices
        )


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
    def __init__(self):
        self.visited = set()

    def transform_product(
        self, ingredient: ProductIngredient, scale: int = 1
    ) -> Ingredient:
        return Ingredient(
            amount=ingredient.amount * scale,
            unit=Unit(ingredient.unit),
            product=ingredient.product,
        )

    def transform_recipe(self, recipe: RecipeModel, scale: int = 1) -> Recipe:
        if recipe in self.visited:
            return Recipe(recipe=recipe, valid=False)
        self.visited.add(recipe)

        return Recipe(
            amount=scale,
            recipe=recipe,
            ingredients=[
                self.transform_product(p, scale=scale)
                for p in recipe.productingredient_set.all()
            ],
            base_recipes=[
                self.transform_recipe(r.base_recipe, scale=scale * r.amount)
                for r in recipe.recipeingredient_set.all()
            ],
        )

    def transform(self, recipe: RecipeModel, scale: int = 1):
        return self.transform_recipe(recipe, scale)
