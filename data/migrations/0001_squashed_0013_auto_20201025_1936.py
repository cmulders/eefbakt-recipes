# Generated by Django 3.2.8 on 2021-10-29 18:44

import data.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("data", "0001_initial"),
        ("data", "0002_auto_20200707_1757"),
        ("data", "0003_auto_20200707_1945"),
        ("data", "0004_auto_20200711_1125"),
        ("data", "0005_auto_20200711_1141"),
        ("data", "0006_auto_20200712_1956"),
        ("data", "0007_auto_20200721_1659"),
        ("data", "0008_auto_20200802_2019"),
        ("data", "0009_auto_20200804_2011"),
        ("data", "0010_auto_20200804_2110"),
        ("data", "0011_auto_20201013_1808"),
        ("data", "0012_auto_20201013_1917"),
        ("data", "0013_auto_20201025_1936"),
    ]

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="ProductIngredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="data.product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "products",
                    models.ManyToManyField(
                        through="data.ProductIngredient", to="data.Product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                (
                    "base_recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base_recipes",
                        to="data.recipe",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="data.recipe"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recipe",
            name="recipes",
            field=models.ManyToManyField(
                through="data.RecipeIngredient", to="data.Recipe"
            ),
        ),
        migrations.AddField(
            model_name="productingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="data.recipe"
            ),
        ),
        migrations.AddField(
            model_name="productingredient",
            name="unit",
            field=models.CharField(
                choices=[("ml", "milliliter"), ("gr", "gram"), ("pcs", "pieces")],
                default="pcs",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="productingredient",
            name="unit",
            field=models.CharField(
                choices=[("mL", "milliliter"), ("g", "gram"), ("pcs", "pieces")],
                default="pcs",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="productingredient",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="data.product"
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="base_recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="base_recipes",
                to="data.recipe",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterModelOptions(
            name="productingredient",
            options={"ordering": ["sort_key"]},
        ),
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={"ordering": ["sort_key"]},
        ),
        migrations.AddField(
            model_name="productingredient",
            name="sort_key",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="sort_key",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="productingredient",
            name="unit",
            field=models.CharField(
                choices=[
                    ("mL", "milliliter"),
                    ("g", "gram"),
                    ("pcs", "stuk"),
                    ("el", "eetlepel"),
                    ("tl", "theelepel"),
                ],
                default="g",
                max_length=5,
            ),
        ),
        migrations.CreateModel(
            name="ProductPrice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("store", models.CharField(blank=True, max_length=80)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("mL", "milliliter"),
                            ("g", "gram"),
                            ("pcs", "stuk"),
                            ("el", "eetlepel"),
                            ("tl", "theelepel"),
                        ],
                        default="g",
                        max_length=5,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="data.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                (
                    "recipe_description",
                    models.TextField(blank=True, verbose_name="Session recipe"),
                ),
                ("session_date", models.DateField(default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-session_date", "-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="SessionRecipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                ("sort_key", models.IntegerField(default=1)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="data.recipe"
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_recipes",
                        to="data.session",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_key"],
            },
        ),
        migrations.CreateModel(
            name="SessionProduct",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("mL", "milliliter"),
                            ("g", "gram"),
                            ("pcs", "stuk"),
                            ("el", "eetlepel"),
                            ("tl", "theelepel"),
                        ],
                        default="g",
                        max_length=5,
                    ),
                ),
                ("sort_key", models.IntegerField(default=1)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="data.product",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredients",
                        to="data.session",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_key"],
            },
        ),
        migrations.AddField(
            model_name="session",
            name="products",
            field=models.ManyToManyField(
                related_name="sessions",
                through="data.SessionProduct",
                to="data.Product",
            ),
        ),
        migrations.AddField(
            model_name="session",
            name="recipes",
            field=models.ManyToManyField(
                related_name="sessions", through="data.SessionRecipe", to="data.Recipe"
            ),
        ),
        migrations.CreateModel(
            name="UnitConversion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "from_unit",
                    models.CharField(
                        choices=[
                            ("mL", "milliliter"),
                            ("g", "gram"),
                            ("pcs", "stuk"),
                            ("el", "eetlepel"),
                            ("tl", "theelepel"),
                        ],
                        default="g",
                        max_length=5,
                    ),
                ),
                ("scale", models.FloatField()),
                (
                    "to_unit",
                    models.CharField(
                        choices=[
                            ("mL", "milliliter"),
                            ("g", "gram"),
                            ("pcs", "stuk"),
                            ("el", "eetlepel"),
                            ("tl", "theelepel"),
                        ],
                        default="mL",
                        max_length=5,
                    ),
                ),
                ("object_id", models.IntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ImageTag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        height_field="height",
                        upload_to=data.models.model_directory_path,
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(blank=True, editable=False, null=True)),
                ("height", models.IntegerField(blank=True, editable=False, null=True)),
                ("name", models.CharField(blank=True, max_length=150)),
                ("caption", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.IntegerField(editable=False)),
                (
                    "content_type",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AlternateImageTag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        height_field="height",
                        upload_to="imagetags/alternates",
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(blank=True, editable=False, null=True)),
                ("height", models.IntegerField(blank=True, editable=False, null=True)),
                (
                    "original",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alternates",
                        to="data.imagetag",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="unitconversion",
            constraint=models.UniqueConstraint(
                fields=("object_id", "content_type", "from_unit", "to_unit"),
                name="unique_conversions",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="unit",
            field=models.CharField(
                choices=[
                    ("mL", "milliliter"),
                    ("g", "gram"),
                    ("pcs", "stuk"),
                    ("el", "eetlepel"),
                    ("tl", "theelepel"),
                ],
                default="pcs",
                max_length=5,
            ),
        ),
    ]