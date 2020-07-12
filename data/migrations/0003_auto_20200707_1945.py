# Generated by Django 3.0.7 on 2020-07-07 19:45

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    ProductIngredient = apps.get_model("data", "productingredient")
    db_alias = schema_editor.connection.alias
    ProductIngredient.objects.using(db_alias).filter(unit="ml").update(unit="mL")
    ProductIngredient.objects.using(db_alias).filter(unit="gr").update(unit="g")


def reverse_func(apps, schema_editor):
    ProductIngredient = apps.get_model("data", "productingredient")
    db_alias = schema_editor.connection.alias
    ProductIngredient.objects.using(db_alias).filter(unit="mL").update(unit="ml")
    ProductIngredient.objects.using(db_alias).filter(unit="g").update(unit="gr")


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_auto_20200707_1757"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        migrations.AlterField(
            model_name="productingredient",
            name="unit",
            field=models.CharField(
                choices=[("mL", "milliliter"), ("g", "gram"), ("pcs", "pieces")],
                default="pcs",
                max_length=5,
            ),
        ),
    ]
