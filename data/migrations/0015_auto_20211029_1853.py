# Generated by Django 3.2.8 on 2021-10-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20201206_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productingredient',
            name='unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='g', max_length=5),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='g', max_length=5),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(related_name='recipes', through='data.ProductIngredient', to='data.Product'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='pcs', max_length=5),
        ),
        migrations.AlterField(
            model_name='sessionproduct',
            name='unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='g', max_length=5),
        ),
        migrations.AlterField(
            model_name='unitconversion',
            name='from_unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='g', max_length=5),
        ),
        migrations.AlterField(
            model_name='unitconversion',
            name='to_unit',
            field=models.CharField(choices=[('-', '-'), ('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel'), ('some', 'snufje'), ('cm', 'cm')], default='mL', max_length=5),
        ),
    ]
