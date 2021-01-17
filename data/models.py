from decimal import Decimal
from pathlib import Path, PurePath
from typing import *

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.files.images import ImageFile
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .constants import Unit

__all__ = ["Product", "Recipe", "ProductIngredient", "RecipeIngredient"]


def model_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    app_model = f"{instance.content_type.app_label}_{instance.content_type.model}"
    return f"imagetags/{app_model}/{filename}"


class ImageTag(models.Model):
    image = models.ImageField(
        width_field="width", height_field="height", upload_to=model_directory_path
    )

    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)

    name = models.CharField(max_length=150, blank=True)
    caption = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object_id = models.IntegerField(editable=False)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False
    )
    object = GenericForeignKey()

    def create_thumbnails(self):
        sizes = {128, 256, 512, 1024, 2048}
        for alternate in self.alternates.all():
            sizes.discard(alternate.width)
            sizes.discard(alternate.height)

        for size in sizes:
            self.make_alternate(size)

    def make_alternate(self, size):
        from io import BytesIO

        from PIL import Image

        im = Image.open(self.image.open())
        im.thumbnail((size, size))
        thumb_image = BytesIO()
        im.save(thumb_image, im.format)

        original_path = PurePath(self.image.name)
        new_name = f"{original_path.stem}_{im.width}x{im.width}{original_path.suffix}"

        image_file = ImageFile(thumb_image, name=new_name)

        self.alternates.create(image=image_file)


class AlternateImageTag(models.Model):
    original = models.ForeignKey(
        ImageTag, related_name="alternates", on_delete=models.CASCADE, editable=False
    )

    image = models.ImageField(
        width_field="width", height_field="height", upload_to="imagetags/alternates"
    )

    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)


@receiver(models.signals.post_delete, sender=AlternateImageTag)
@receiver(models.signals.post_delete, sender=ImageTag)
def delete_image(sender, **kwargs):
    """
    Delete the uploaded file.
    """
    instance = kwargs["instance"]

    if instance.image:
        instance.image.delete(save=False)


@receiver(models.signals.post_init, sender=AlternateImageTag)
def cleanup_removed(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.pk and not Path(instance.image.path).exists():
        instance.delete()


@receiver(models.signals.post_save, sender=ImageTag)
def create_thumbnails(sender, **kwargs):
    instance = kwargs["instance"]
    instance.create_thumbnails()


class UnitConversion(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["object_id", "content_type", "from_unit", "to_unit"],
                name="unique_conversions",
            )
        ]

    from_unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    scale = models.FloatField()
    to_unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.ML)

    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = GenericForeignKey()

    def __str__(self):
        return f"{self.object}: 1 {Unit(self.from_unit).short_name} = {self.scale} {Unit(self.to_unit).short_name}"


class Product(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=150, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prices: List["ProductPrice"]

    unit_conversions = GenericRelation(UnitConversion, related_name="+")

    def get_absolute_url(self):
        return reverse("data:product-detail", args=[self.pk])

    def __str__(self):
        return self.name

    def __repr__(self):
        return _("Product: %(name)s") % {"name": self.name}


class ProductPrice(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="prices"
    )

    store = models.CharField(max_length=80, blank=True)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    @property
    def normalized_price(self) -> Decimal:
        return self.price / self.amount


class ProductIngredient(models.Model):

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    base_recipe = models.ForeignKey(
        "Recipe", on_delete=models.PROTECT, related_name="base_recipes"
    )

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class Recipe(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.PIECE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(
        "Product", through=ProductIngredient, related_name="recipes"
    )
    productingredient_set: List[ProductIngredient]

    recipes = models.ManyToManyField(
        "Recipe",
        through=RecipeIngredient,
        through_fields=(
            "recipe",
            "base_recipe",
        ),
    )
    recipeingredient_set: List[RecipeIngredient]

    images = GenericRelation(ImageTag, related_name="+")

    @property
    def title(self):
        base_str = self.name
        if self.amount is not None and self.unit:
            base_str += f" ({float(self.amount):g} {Unit(self.unit).short_name})"
        return base_str

    def __str__(self):
        return self.title

    def __repr__(self):
        return _("Recipe: %(name)s") % {"name": self.name}

    def get_absolute_url(self):
        return reverse("data:recipe-detail", args=[self.pk])


class SessionProduct(models.Model):
    session = models.ForeignKey(
        "Session", related_name="ingredients", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.GR)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class SessionRecipe(models.Model):
    session = models.ForeignKey(
        "Session", related_name="session_recipes", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)

    amount = models.DecimalField(default=1, max_digits=10, decimal_places=3)
    sort_key = models.IntegerField(default=1)

    class Meta:
        ordering = ["sort_key"]


class Session(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    recipe_description = models.TextField("Session recipe", blank=True)

    session_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipes = models.ManyToManyField(
        Recipe, through=SessionRecipe, related_name="sessions"
    )
    products = models.ManyToManyField(
        Product, through=SessionProduct, related_name="sessions"
    )

    images = GenericRelation(ImageTag, related_name="+")

    def __str__(self):
        return self.title

    def __repr__(self):
        return _("Session: %(title)s") % {"title": self.title}

    def get_absolute_url(self):
        return reverse("data:session-detail", args=[self.pk])

    class Meta:
        ordering = ["-session_date", "-updated_at"]
