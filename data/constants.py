from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.TextChoices):
    ML = "mL", _("milliliter")
    GR = "g", _("gram")
    PIECE = "pcs", _("stuk")
    TBSP = "el", _("eetlepel")
    TSP = "tl", _("theelepel")
