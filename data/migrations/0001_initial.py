# Generated by Django 3.0.7 on 2020-07-05 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('unit', models.CharField(choices=[('ml', 'milliliter'), ('gr', 'gram'), ('pcs', 'pieces')], default='pcs', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('products', models.ManyToManyField(through='data.ProductIngredient', to='data.Product')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('base_recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_recipes', to='data.Recipe')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipes',
            field=models.ManyToManyField(through='data.RecipeIngredient', to='data.Recipe'),
        ),
        migrations.AddField(
            model_name='productingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Recipe'),
        ),
    ]
