from typing import Mapping

from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.TextChoices):
    EMPTY = "-", "-"
    ML = "mL", _("milliliter")
    GR = "g", _("gram")
    PIECE = "pcs", _("stuk")
    TBSP = "el", _("eetlepel")
    TSP = "tl", _("theelepel")
    SOME = "some", _("snufje")
    CM = "cm", _("cm")
    PORTION = "ptn", _("portie")


    @property
    def no_quantity(self):
        return self in (self.SOME, )

    @property
    def short_name(self):
        short_names = {
            str(self.PIECE.value): "stuk",
            str(self.SOME.value): "snufje",
            str(self.PORTION.value): "portie",
            str(self.EMPTY.value): "",
        }
        return short_names.get(self.value, self.value)

    def __lt__(self, other: "Unit") -> bool:
        """
        Sort the enum value on index
        """
        if isinstance(other, type(self)):
            member_list = list(self.__class__)
            return member_list.index(self) < member_list.index(other)

        return super().__lt__(other)
