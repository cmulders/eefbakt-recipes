from django import template
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from utils import fraction

register = template.Library()


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
