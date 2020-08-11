from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.TextChoices):
    ML = "mL", _("milliliter")
    GR = "g", _("gram")
    PIECE = "pcs", _("stuk")
    TBSP = "el", _("eetlepel")
    TSP = "tl", _("theelepel")

    @staticmethod
    def norm_unit(value):
        casted = Unit(value)
        if casted in [Unit.GR, Unit.ML]:
            return (Unit.GR, Unit.ML)
        else:
            return (casted,)

    def __eq__(self, other):
        return super().__eq__(other) or self.norm_unit == other.norm_unit

    @property
    def short_name(self):
        return {self.PIECE.value: "stk",}.get(self.value, self.value)
