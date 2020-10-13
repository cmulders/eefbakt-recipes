# Generated by Django 3.1 on 2020-10-13 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("baking", "0011_auto_20200811_2048"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name="sessionproduct", name="product",),
                migrations.RemoveField(model_name="sessionproduct", name="session",),
                migrations.RemoveField(model_name="sessionrecipe", name="recipe",),
                migrations.RemoveField(model_name="sessionrecipe", name="session",),
                migrations.DeleteModel(name="Session",),
                migrations.DeleteModel(name="SessionProduct",),
                migrations.DeleteModel(name="SessionRecipe",),
            ],
            database_operations=[
                migrations.AlterModelTable(name="Session", table="data_session",),
                migrations.AlterModelTable(
                    name="SessionProduct", table="data_sessionproduct",
                ),
                migrations.AlterModelTable(
                    name="SessionRecipe", table="data_sessionrecipe",
                ),
            ],
        )
    ]