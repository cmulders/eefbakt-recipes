import re
from fractions import Fraction
from numbers import Real

from django.template.library import parse_bits


def format_fraction(real: Real, limit_denominator=10) -> str:
    frac_real = Fraction(real)
    frac = frac_real.limit_denominator(limit_denominator)

    offset = float(frac_real / frac)
    if offset < 0.99:
        raise ValueError(
            f"Could not convert with enough precision. (Off by {1-offset:.1%})"
        )

    nom, denom = frac.as_integer_ratio()
    prefix, nom = divmod(nom, denom)

    out = ""

    if prefix:
        out += f"{prefix} "

    if nom:
        out += f"{nom}/{denom}"

    return out


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
