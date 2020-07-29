from django.contrib import admin

from .models import ImageTag


# Register your models here.
@admin.register(ImageTag)
class ImageTagAdmin(admin.ModelAdmin):
    pass
