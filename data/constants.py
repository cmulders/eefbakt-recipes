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
