# Generated by Django 3.0.7 on 2020-07-12 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='name',
            new_name='title',
        ),
    ]
