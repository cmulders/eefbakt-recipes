# Generated by Django 3.2.8 on 2021-10-31 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_auto_20211029_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='kind',
            field=models.CharField(choices=[('sweet', 'Zoet'), ('savory', 'Hartig'), ('bread', 'Brood')], default='sweet', max_length=10),
        ),
        migrations.AddField(
            model_name='session',
            name='kind',
            field=models.CharField(choices=[('sweet', 'Zoet'), ('savory', 'Hartig'), ('bread', 'Brood')], default='sweet', max_length=10),
        ),
    ]
