from functools import partial
from os import read

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html

from .models import ImageTag, UnitConversion


def thumbnail(obj, width=500, height=500):
    return format_html(
        '<img src="{}" style="width: {}px; height:{}px; border-radius:5px" />',
        obj.image.url,
        int(width),
        int(height),
    )


thumbnail.__name__ = "Thumbnail"

tiny_thumbnail = partial(thumbnail, width=50, height=50)
tiny_thumbnail.__name__ = thumbnail.__name__

small_thumbnail = partial(thumbnail, width=150, height=150)
small_thumbnail.__name__ = thumbnail.__name__


def image_spec(obj):
    try:
        dims = f"{getattr(obj, 'width', '?')} × {getattr(obj, 'height', '?')}"
        size = filesizeformat(obj.image.size)
        return f"{dims} — {size}"
    except FileNotFoundError:
        return "(not found)"


# Register your models here.
@admin.register(ImageTag)
class ImageTagAdmin(admin.ModelAdmin):
    list_display = (
        "related_object",
        small_thumbnail,
        image_spec,
        "name",
    )
    list_display_links = (small_thumbnail, image_spec, "name")

    fields = (thumbnail, "image", image_spec, "name", "caption")
    readonly_fields = (thumbnail, image_spec)

    def related_object(self, obj):
        return str(obj.object)

    related_object.short_description = "Object"


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    pass
