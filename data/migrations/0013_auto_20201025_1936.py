# Generated by Django 3.1.2 on 2020-10-25 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_auto_20201013_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='unit',
            field=models.CharField(choices=[('mL', 'milliliter'), ('g', 'gram'), ('pcs', 'stuk'), ('el', 'eetlepel'), ('tl', 'theelepel')], default='pcs', max_length=5),
        ),
    ]
