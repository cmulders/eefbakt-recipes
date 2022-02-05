from django import template
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from utils import fraction

register = template.Library()


@register.filter(is_safe=True)
def sigformat(value, significance=3) -> str:
    significance = int(significance)

    # Round value if within .1% accuracy
    value = round(value) if 0.001 > abs(1 - round(value) / value) else value

    try:
        frac = fraction.ExtFraction(value)
        prefix, nom, denom = frac.limit_denominator(10).as_tuple()
    except ValueError:
        value = float(f"{value:.{-significance}g}")
        return defaultfilters.floatformat(value, significance)

    decimal_digits = significance - len(str(prefix or ""))
    if nom and decimal_digits > 0:
        decimal = round(nom / denom * pow(10, decimal_digits))
        if decimal == 0:
            return f"{prefix}"
        return f"{prefix}.{decimal}"
    else:
        return f"{prefix}"


@register.filter(is_safe=True)
def fractionformat_html(value, significance=-3) -> str:
    significance = int(significance)
    significance_abs = abs(significance)
    try:
        frac = fraction.ExtFraction(value)
        prefix, nom, denom = frac.limit_denominator(10).as_tuple()
    except ValueError:
        value = float(f"{value:.{significance_abs}g}")
        return defaultfilters.floatformat(value, significance)

    prefix = str(prefix) if prefix else ""
    fraction_str = (
        f"<sup>{nom}</sup>&frasl;<sub>{denom}</sub>"
        if nom and len(prefix) < significance_abs
        else ""
    )
    return mark_safe(f"{prefix} {fraction_str}".strip())


@register.filter(is_safe=True)
def fractionformat(value, errors="ignore") -> str:
    try:
        frac = fraction.ExtFraction(value)
        prefix, nom, denom = frac.limit_denominator(10).as_tuple()
    except ValueError:
        if errors == "raise":
            raise
        return str(value)

    prefix = str(prefix) if prefix else ""
    fraction_str = f"{nom}/{denom}" if nom else ""
    return f"{prefix} {fraction_str}".strip()
