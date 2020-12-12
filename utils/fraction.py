import re
from fractions import Fraction
from numbers import Real
from typing import Optional, Tuple

from django.template.library import parse_bits


def as_fraction(real: Real, limit_denominator=10) -> Fraction:
    frac_real = Fraction(real)
    frac = frac_real.limit_denominator(limit_denominator)

    offset = float(frac_real / frac)
    if offset < 0.99:
        raise ValueError(
            f"Could not convert with enough precision. (Off by {1-offset:.1%})"
        )

    return frac


def as_tuple(frac: Fraction) -> Tuple[Optional[int], int, int]:
    if not isinstance(frac, Fraction):
        raise ValueError("Not a fraction")

    nom, denom = frac.as_integer_ratio()
    prefix, nom = divmod(nom, denom)

    return (prefix or None, nom, denom)


def parse_fraction(literal: str, limit_denominator=10) -> Fraction:
    match = re.match("\s*(:?(?P<whole>\d+)\s)?(?P<frac>\d+/\d+)\s*", literal)

    if not match:
        raise ValueError("Not a fraction")

    frac_real = Fraction(match.group("frac")) + int(match.group("whole") or 0)
    frac = frac_real.limit_denominator(limit_denominator)

    offset = float(frac_real / frac)
    if offset < 0.99:
        raise ValueError(
            f"Could not convert with enough precision. (Off by {1-offset:.1%})"
        )

    return frac
