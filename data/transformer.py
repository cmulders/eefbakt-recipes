from enum import Enum

from .models import Ingredient, Product, Recipe


class Leaf(Enum):
    RECIPE = "recipe"
    PRODUCT = "product"


class RecipeTreeTransformer:
    @property
    def visitors(self):
        return {
            Product: self.visit_product,
            Recipe: self.visit_recipe,
        }

    def visit_product(self, product: Product) -> tuple:
        return (Leaf.PRODUCT.value, product.name, product.size)

    def visit_ingredient(self, ingredient: Ingredient) -> tuple:
        instance = ingredient.ingredient_object

        return (ingredient.amount,) + self.visit_object(instance)

    def visit_recipe(self, recipe: Recipe) -> tuple:
        objects = [self.visit_ingredient(i) for i in recipe.ingredients.all()]
        return (Leaf.RECIPE.value, recipe.name, objects)

    def visit_object(self, obj):
        visitor = self.visitors.get(obj.__class__)
        if not visitor:
            raise NotImplementedError
        return visitor(obj)

    def transform(self, recipe) -> tuple:
        assert isinstance(recipe, Recipe)
        return self.visit_recipe(recipe)
