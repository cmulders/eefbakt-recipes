from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..constants import Unit


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
