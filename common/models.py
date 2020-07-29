import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver


def model_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    app_model = f"{instance.content_type.app_label}_{instance.content_type.model}"
    return f"imagetags/{app_model}/{filename}"


class ImageTag(models.Model):
    image = models.ImageField(upload_to=model_directory_path)

    name = models.CharField(max_length=150)
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
