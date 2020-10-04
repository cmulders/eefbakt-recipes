from functools import partial
from os import read

from django.contrib import admin
from django.template.defaultfilters import filesizeformat, unordered_list
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import AlternateImageTag, ImageTag, UnitConversion


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
class AlternateImageTagInline(admin.TabularInline):
    extra = 0
    model = AlternateImageTag

    fields = (
        tiny_thumbnail,
        image_spec,
        "image",
    )
    readonly_fields = (
        tiny_thumbnail,
        image_spec,
    )


@admin.register(ImageTag)
class ImageTagAdmin(admin.ModelAdmin):
    inlines = [AlternateImageTagInline]

    list_display = (
        "related_object",
        small_thumbnail,
        image_spec,
        "alternatives",
        "name",
    )
    list_display_links = (small_thumbnail, image_spec, "name")

    fields = (thumbnail, "image", image_spec, "name", "caption")
    readonly_fields = (thumbnail, image_spec)

    actions = ["make_thumbnails"]

    def related_object(self, obj):
        return str(obj.object)

    related_object.short_description = "Object"

    def alternatives(self, obj):
        return mark_safe(
            "<ul>"
            + unordered_list([image_spec(alt) for alt in obj.alternates.all()])
            + "</ul>"
        )

    def make_thumbnails(self, request, queryset):
        instance: ImageTag
        for instance in queryset.prefetch_related("alternates").all():
            instance.create_thumbnails()

    make_thumbnails.short_description = "Create thumbnails for selected images"


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    pass
