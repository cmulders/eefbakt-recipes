import re
from fractions import Fraction
from numbers import Real
from typing import Optional, Tuple

from django.template.library import parse_bits


class ExtFraction(Fraction):
    def limit_denominator(self, max_denominator: int) -> Fraction:
        limited = super().limit_denominator(max_denominator)

        if limited == 0:
            # Pevent a division by zero below
            raise ValueError(f"Could not convert with enough precision.")

        offset = float(self / limited)
        if offset < 0.99:
            raise ValueError(
                f"Could not convert with enough precision. (Off by {1-offset:.1%})"
            )

        return ExtFraction(limited)

    def as_tuple(self) -> Tuple[Optional[int], int, int]:
        nom, denom = self.as_integer_ratio()
        prefix, nom = divmod(nom, denom)

        return (prefix or None, nom, denom)

    @classmethod
    def parse_str(cls, literal: str, limit_denominator=10):
        match = re.match("\s*(:?(?P<whole>\d+)\s)?(?P<frac>\d+/\d+)\s*", literal)

        if not match:
            raise ValueError("Not a fraction")

        frac_real = cls(match.group("frac")) + int(match.group("whole") or 0)
        return frac_real.limit_denominator(limit_denominator)


def as_fraction(real: Real, limit_denominator: int = 10) -> Fraction:
    return ExtFraction(real).limit_denominator(limit_denominator)


def as_tuple(frac: Fraction) -> Tuple[Optional[int], int, int]:
    return ExtFraction(frac).as_tuple()


def parse_fraction(literal: str, limit_denominator=10) -> Fraction:
    return ExtFraction.parse_str(literal, limit_denominator)
