import os
from pathlib import Path, PurePath

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.images import ImageFile
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

    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)

    name = models.CharField(max_length=150, blank=True)
    caption = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object_id = models.IntegerField(editable=False)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False
    )
    object = GenericForeignKey()

    def make_alternate(self, size):
        from io import BytesIO

        from PIL import Image

        im = Image.open(self.image.open())
        im.thumbnail((size, size))
        thumb_image = BytesIO()
        im.save(thumb_image, im.format)

        original_path = PurePath(self.image.name)
        new_name = f"{original_path.stem}_{im.width}x{im.width}{original_path.suffix}"

        image_file = ImageFile(thumb_image, name=new_name)

        self.alternates.create(image=image_file)


class AlternateImageTag(models.Model):
    original = models.ForeignKey(
        ImageTag, related_name="alternates", on_delete=models.CASCADE, editable=False
    )

    image = models.ImageField(
        width_field="width", height_field="height", upload_to="imagetags/alternates"
    )

    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)


@receiver(models.signals.post_delete, sender=AlternateImageTag)
@receiver(models.signals.post_delete, sender=ImageTag)
def delete_image(sender, **kwargs):
    """
    Delete the uploaded file.
    """
    instance = kwargs["instance"]

    if instance.image:
        instance.image.delete(save=False)


@receiver(models.signals.post_init, sender=AlternateImageTag)
def cleanup_removed(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.pk and not Path(instance.image.path).exists():
        instance.delete()


@receiver(models.signals.post_save, sender=ImageTag)
def create_thumbnails(sender, **kwargs):
    instance = kwargs["instance"]

    sizes = {128, 256, 512, 1024, 2048}
    for alternate in instance.alternates.all():
        sizes.discard(alternate.width)
        sizes.discard(alternate.height)

    for size in sizes:
        instance.make_alternate(size)


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
