# Generated by Django 3.0.8 on 2020-08-11 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baking', '0010_session_recipe_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='recipe_description',
            field=models.TextField(blank=True, verbose_name='Session recipe'),
        ),
    ]