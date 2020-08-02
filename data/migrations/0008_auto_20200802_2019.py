# Generated by Django 3.0.8 on 2020-08-02 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20200721_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productingredient',
            options={'ordering': ['sort_key']},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ['sort_key']},
        ),
        migrations.AddField(
            model_name='productingredient',
            name='sort_key',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='sort_key',
            field=models.IntegerField(default=1),
        ),
    ]