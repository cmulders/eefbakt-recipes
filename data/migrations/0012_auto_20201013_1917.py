# Generated by Django 3.1 on 2020-10-13 19:17

import data.models
import django.db.models.deletion
from django.db import migrations, models


def update_common_contentypes(apps, schema_editor):
    """
    Updates content types.
    We want to have the same content type id, when the model is moved.
    """
    ContentType = apps.get_model("contenttypes", "ContentType")
    db_alias = schema_editor.connection.alias

    models = [
        "alternateimagetag",
        "imagetag",
        "unitconversion",
    ]
    ContentType.objects.using(db_alias).filter(
        app_label="common", model__in=models
    ).update(app_label="data")


def update_common_contentypes_reverse(apps, schema_editor):
    """
    Reverts changes in content types.
    """
    ContentType = apps.get_model("contenttypes", "ContentType")
    db_alias = schema_editor.connection.alias

    models = [
        "alternateimagetag",
        "imagetag",
        "unitconversion",
    ]
    ContentType.objects.using(db_alias).filter(
        app_label="data", model__in=models
    ).update(app_label="common")


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("data", "0011_auto_20201013_1808"),
        ("common", "0009_auto_20201013_1917"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="UnitConversion",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "from_unit",
                            models.CharField(
                                choices=[
                                    ("mL", "milliliter"),
                                    ("g", "gram"),
                                    ("pcs", "stuk"),
                                    ("el", "eetlepel"),
                                    ("tl", "theelepel"),
                                ],
                                default="g",
                                max_length=5,
                            ),
                        ),
                        ("scale", models.FloatField()),
                        (
                            "to_unit",
                            models.CharField(
                                choices=[
                                    ("mL", "milliliter"),
                                    ("g", "gram"),
                                    ("pcs", "stuk"),
                                    ("el", "eetlepel"),
                                    ("tl", "theelepel"),
                                ],
                                default="mL",
                                max_length=5,
                            ),
                        ),
                        ("object_id", models.IntegerField()),
                        (
                            "content_type",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="contenttypes.contenttype",
                            ),
                        ),
                    ],
                ),
                migrations.CreateModel(
                    name="ImageTag",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "image",
                            models.ImageField(
                                height_field="height",
                                upload_to=data.models.model_directory_path,
                                width_field="width",
                            ),
                        ),
                        (
                            "width",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        (
                            "height",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        ("name", models.CharField(blank=True, max_length=150)),
                        ("caption", models.TextField(blank=True)),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                        ("object_id", models.IntegerField(editable=False)),
                        (
                            "content_type",
                            models.ForeignKey(
                                editable=False,
                                on_delete=django.db.models.deletion.CASCADE,
                                to="contenttypes.contenttype",
                            ),
                        ),
                    ],
                ),
                migrations.CreateModel(
                    name="AlternateImageTag",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "image",
                            models.ImageField(
                                height_field="height",
                                upload_to="imagetags/alternates",
                                width_field="width",
                            ),
                        ),
                        (
                            "width",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        (
                            "height",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        (
                            "original",
                            models.ForeignKey(
                                editable=False,
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="alternates",
                                to="data.imagetag",
                            ),
                        ),
                    ],
                ),
                migrations.AddConstraint(
                    model_name="unitconversion",
                    constraint=models.UniqueConstraint(
                        fields=("object_id", "content_type", "from_unit", "to_unit"),
                        name="unique_conversions",
                    ),
                ),
            ],
            database_operations=[
                migrations.RunPython(
                    update_common_contentypes, update_common_contentypes_reverse
                )
            ],
        ),
    ]
