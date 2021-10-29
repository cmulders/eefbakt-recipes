from django.test import TestCase

from .models import Product, Recipe


class RecipeTest(TestCase):
    def test_recipe_has_products(self):
        p = Product.objects.create(name="Product")
        r = Recipe.objects.create(name="Recept")

        r.products.add(p, through_defaults={"amount": 100})

        ingredient = r.productingredient_set.select_related("product").first()

        self.assertEqual(ingredient.amount, 100)
        self.assertEqual(ingredient.product, p)

    def test_recipe_has_recipes(self):
        p = Product.objects.create(name="Product")
        base_recipe = Recipe.objects.create(name="Basis Recept")
        r = Recipe.objects.create(name="Recept")

        base_recipe.products.add(p, through_defaults={"amount": 50})
        r.products.add(p, through_defaults={"amount": 100})
        r.recipes.add(base_recipe, through_defaults={"amount": 200})

        ingredient = r.productingredient_set.select_related("product").first()

        self.assertEqual(ingredient.amount, 100)
        self.assertEqual(ingredient.product, p)

        recipe_ingredient = r.recipeingredient_set.select_related("recipe").first()

        self.assertEqual(recipe_ingredient.amount, 200)
        self.assertEqual(recipe_ingredient.base_recipe, base_recipe)
