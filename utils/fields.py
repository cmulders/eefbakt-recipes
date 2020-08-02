from django import forms
from django.core.exceptions import ImproperlyConfigured


class CreatingModelChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, *args, creation_field=None, **kwargs):
        opts = queryset.model._meta
        model_field_names = [f.name for f in opts.get_fields()]

        if not creation_field:
            raise ImproperlyConfigured(
                f"'creation_field' should not be empty, but one of {', '.join(model_field_names)}"
            )
        if not creation_field in model_field_names:
            raise ImproperlyConfigured(
                f"'{creation_field}' should be one of {','.join(model_field_names)}"
            )

        self.creation_field = creation_field

    def to_python(self, value):
        try:
            return super().to_python(value)
        except forms.ValidationError as err:
            if err.code != "invalid_choice":
                raise  # Reraise the Validation error, only invalid choice we handle

        # Create a new model on the fly
        return self.queryset.model.objects.create(**{self.creation_field: value})
