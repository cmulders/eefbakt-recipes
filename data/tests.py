from decimal import Decimal

from django.test import TestCase

from .models import Ingredient, Product, Recipe
from .transformer import RecipeTreeTransformer


class RecipeTest(TestCase):
    def test_recipe_has_ingredients(self):
        product1 = Product.objects.create(name="Product1", unit=Product.Unit.PIECE)
        product2 = Product.objects.create(name="Product2", unit=Product.Unit.PIECE)
        recipe = Recipe.objects.create(name="Recipe")

        recipe.ingredients.create(ingredient_object=product1, amount=2)
        recipe.ingredients.create(ingredient_object=product2, amount=0.5)

        self.assertEqual(
            recipe.as_str(),
            """# Recipe
  2.00 pcs - Product1
  0.50 pcs - Product2""",
        )

    def test_recipe_has_recipes(self):
        product1 = Product.objects.create(name="Product1", unit=Product.Unit.PIECE)
        product2 = Product.objects.create(name="Product2", unit=Product.Unit.PIECE)
        product3 = Product.objects.create(name="Product3", unit=Product.Unit.PIECE)

        base_base_recipe = Recipe.objects.create(name="BaseBaseRecipe")
        base_base_recipe.ingredients.create(ingredient_object=product3, amount=4)

        base_recipe = Recipe.objects.create(name="BaseRecipe")
        base_recipe.ingredients.create(ingredient_object=product1, amount=2)
        base_recipe.ingredients.create(ingredient_object=base_base_recipe, amount=1)
        base_recipe.ingredients.create(ingredient_object=product2, amount=0.5)

        recipe = Recipe.objects.create(name="Recipe")
        recipe.ingredients.create(ingredient_object=base_recipe, amount=4)
        recipe.ingredients.create(ingredient_object=product3, amount=3)

        self.assertEqual(
            recipe.as_str(),
            """# Recipe
  # BaseRecipe
    8.00 pcs - Product1
    # BaseBaseRecipe
      16.00 pcs - Product3
    2.00 pcs - Product2
  3.00 pcs - Product3""",
        )

    def test_deletion_cascades(self):
        product1 = Product.objects.create(
            name="Product1", size=1, unit=Product.Unit.PIECE
        )
        product2 = Product.objects.create(
            name="Product2", size=1, unit=Product.Unit.PIECE
        )
        base_recipe = Recipe.objects.create(name="BaseRecipe")
        base_recipe.ingredients.create(ingredient_object=product1, amount=2)
        base_recipe.ingredients.create(ingredient_object=product2, amount=0.5)

        recipe = Recipe.objects.create(name="Recipe")
        recipe.ingredients.create(ingredient_object=base_recipe, amount=4)
        recipe.ingredients.create(ingredient_object=product1, amount=3)


class RecipeTreeTransformerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.bulk_create(
            [
                Product(name="Product1", unit=Product.Unit.PIECE),
                Product(name="Product2", unit=Product.Unit.GR),
            ]
        )
        cls.products = Product.objects.all()

        cls.base = Recipe.objects.create(name="BaseRecipe")
        cls.recipe = Recipe.objects.create(name="Recipe")
        p = cls.products
        ingredients = [
            Ingredient(recipe=cls.base, ingredient_object=p[0], amount=1),
            Ingredient(recipe=cls.base, ingredient_object=p[1], amount=400),
            Ingredient(recipe=cls.recipe, ingredient_object=cls.base, amount=1),
            Ingredient(recipe=cls.recipe, ingredient_object=p[0], amount=2),
            Ingredient(recipe=cls.recipe, ingredient_object=p[1], amount=200),
        ]
        Ingredient.objects.bulk_create(ingredients)

    def test_transformer(self):
        transfomer = RecipeTreeTransformer()
        self.assertEqual(
            transfomer.transform(self.recipe),
            (
                "recipe",
                "Recipe",
                [
                    (
                        Decimal("1"),
                        "recipe",
                        "BaseRecipe",
                        [
                            (Decimal("1"), "product", "Product1"),
                            (Decimal("400"), "product", "Product2"),
                        ],
                    ),
                    (Decimal("2"), "product", "Product1"),
                    (Decimal("200"), "product", "Product2"),
                ],
            ),
        )
