from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.TextChoices):
    ML = "mL", _("milliliter")
    GR = "g", _("gram")
    PIECE = "pcs", _("stuk")
    TBSP = "el", _("eetlepel")
    TSP = "tl", _("theelepel")

    @property
    def short_name(self):
        return {self.PIECE.value: "stk",}.get(self.value, self.value)

    def __lt__(self, other: "Unit") -> bool:
        """
        Sort the enum value on index
        """
        if isinstance(other, type(self)):
            member_list = list(self.__class__)
            return member_list.index(self) < member_list.index(other)

        return super().__lt__(other)
