from django import template
from utils import fraction

register = template.Library()


@register.filter
def fractionformat(value) -> str:
    return fraction.format_fraction(value)
