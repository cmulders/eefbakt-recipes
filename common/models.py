import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver

from common.constants import Unit


def model_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    app_model = f"{instance.content_type.app_label}_{instance.content_type.model}"
    return f"imagetags/{app_model}/{filename}"


class ImageTag(models.Model):
    image = models.ImageField(
        width_field="width", height_field="height", upload_to=model_directory_path
    )

    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    name = models.CharField(max_length=150, blank=True)
    caption = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = GenericForeignKey()


@receiver(models.signals.post_delete, sender=ImageTag)
def delete_image(sender, **kwargs):
    """
    Delete the uploaded file.
    """
    instance = kwargs["instance"]

    if instance.image:
        instance.image.delete(save=False)


class UnitConversion(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["object_id", "content_type", "from_unit", "to_unit"],
                name="unique_conversions",
            )
        ]

    from_unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    scale = models.FloatField()
    to_unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.ML)

    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = GenericForeignKey()

    def __str__(self):
        return f"{self.object}: 1 {Unit(self.from_unit).short_name} = {self.scale} {Unit(self.to_unit).short_name}"
