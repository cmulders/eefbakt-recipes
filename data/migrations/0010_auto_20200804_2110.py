# Generated by Django 3.0.8 on 2020-08-04 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20200804_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='data.Product'),
        ),
    ]
