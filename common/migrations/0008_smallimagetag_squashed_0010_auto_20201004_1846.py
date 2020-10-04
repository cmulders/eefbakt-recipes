# Generated by Django 3.1 on 2020-10-04 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('common', '0008_smallimagetag'), ('common', '0009_auto_20201004_1435'), ('common', '0010_auto_20201004_1846')]

    dependencies = [
        ('common', '0007_auto_20200819_1600'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetag',
            name='content_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='imagetag',
            name='height',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='imagetag',
            name='object_id',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='imagetag',
            name='width',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.CreateModel(
            name='AlternateImageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='height', upload_to='imagetags/alternates', width_field='width')),
                ('width', models.IntegerField(blank=True, editable=False, null=True)),
                ('height', models.IntegerField(blank=True, editable=False, null=True)),
                ('original', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='alternates', to='common.imagetag')),
            ],
        ),
    ]
