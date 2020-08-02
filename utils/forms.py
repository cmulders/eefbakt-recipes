from django import forms
from django.forms.formsets import ORDERING_FIELD_NAME


class OrderdedModelForm(forms.ModelForm):
    sort_field = "sort_key"

    def save(self, *args, **kwargs):
        if ORDERING_FIELD_NAME in self.cleaned_data and self.sort_field:
            ordering = self.cleaned_data.get(ORDERING_FIELD_NAME, 1) or 1

            setattr(self.instance, self.sort_field, ordering)

        return super().save(*args, **kwargs)
