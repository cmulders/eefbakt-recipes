from django import forms
from django.contrib.contenttypes import forms as generic_forms

from .models import ImageTag


class ImageInput(forms.FileInput):
    template_name = "common/forms/widgets/imagefile.html"

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value


class ImageTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["image"].disabled = True

    class Meta:
        widgets = {
            "image": ImageInput(),
            "caption": forms.TextInput(),
        }


ImageTagInlineFormset = generic_forms.generic_inlineformset_factory(
    ImageTag, form=ImageTagForm, extra=1, max_num=3,
)
