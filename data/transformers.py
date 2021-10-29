from dataclasses import dataclass, field, replace
from decimal import Decimal
from functools import cached_property
from typing import *

from .constants import Unit
from .converters import UnitConverter
from .models import Product, ProductIngredient
from .models import Recipe as RecipeModel


@dataclass(frozen=True, order=True, eq=True)
class Ingredient:
    name: str
    amount: int = field(hash=False)
    unit: Unit
    product: Product = field(compare=False)

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented

        return (
            self.unit == other.unit
            or self.unit_converter.has_conversion(self.unit, other.unit)
        ) and self.product == other.product

    def __add__(self, other: Optional["Ingredient"]):
        if other is None:
            return self

        assert isinstance(other, Ingredient) and self == other

        # Select most appropiate unit to convert to
        to_unit = max(self.unit, other.unit)

        return replace(
            self,
            amount=other._convert_amount(to_unit) + self._convert_amount(to_unit),
            unit=to_unit,
        )

    __radd__ = __add__

    @cached_property
    def unit_converter(self):
        return UnitConverter(self.product.unit_conversions.all())

    def _convert_amount(self, to_unit: Unit) -> Decimal:
        assert self.unit_converter.has_conversion(self.unit, to_unit)

        return self.amount * Decimal(self.unit_converter.scale(self.unit, to_unit))

    @property
    def price(self):
        prices = [
            float(price.normalized_price * self.amount)
            * self.unit_converter.scale(self.unit, price.unit)
            for price in self.product.prices.all()
            if self.unit_converter.has_conversion(price.unit, self.unit)
        ]
        return min(
            prices,
            default=None,
        )


@dataclass
class Recipe:
    name: str = "Unknown"
    description: str = ""
    url: str = None
    base_amount: Optional[int] = None
    scale: int = 1
    unit: Optional[Unit] = None
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

    @property
    def amount(self):
        if self.base_amount is None:
            return self.scale

        if self.unit == Unit.CM:
            return f"{self.scale} x {self.base_amount}"

        return self.base_amount * self.scale


class RecipeTreeTransformer:
    def __init__(self):
        self.visited = set()

    def transform_product(
        self, ingredient: ProductIngredient, scale: int = 1
    ) -> Ingredient:
        return Ingredient(
            name=ingredient.product.name,
            amount=ingredient.amount * scale,
            unit=Unit(ingredient.unit),
            product=ingredient.product,
        )

    def transform_recipe(self, recipe: RecipeModel, scale: int = 1) -> Recipe:
        return Recipe(
            name=recipe.name,
            description=recipe.description,
            url=recipe.get_absolute_url(),
            base_amount=recipe.amount,
            scale=scale,
            unit=Unit(recipe.unit) if recipe.amount is not None else None,
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
