import warnings
from typing import Iterable

from django import template
from django.utils.safestring import mark_safe

from ..models import AlternateImageTag, ImageTag

register = template.Library()


@register.filter
def srcset(value, size=None):
    if not isinstance(value, ImageTag):
        warnings.warn("Srcset filter got something than an ImageTag.")
        return ""

    alternatives: Iterable[AlternateImageTag] = value.alternates.all()

    return ", ".join(
        [f"{image.image.url} {image.width}w" for image in alternatives if image.image]
    )
