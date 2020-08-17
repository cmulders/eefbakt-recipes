from django.contrib import admin

from .models import ImageTag, UnitConversion


# Register your models here.
@admin.register(ImageTag)
class ImageTagAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    pass
