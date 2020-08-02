from django import forms
from django.core.exceptions import ImproperlyConfigured


class CreatingModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        self.creation_field = kwargs.pop("creation_field")

        super().__init__(*args, **kwargs)

        opts = self.queryset.model._meta
        model_field_names = [f.name for f in opts.get_fields()]

        if not self.creation_field in model_field_names:
            raise ImproperlyConfigured(
                f"'{self.creation_field}' should be one of {','.join(model_field_names)}"
            )

    def to_python(self, value):
        try:
            return super().to_python(value)
        except forms.ValidationError as err:
            if err.code != "invalid_choice":
                raise  # Reraise the Validation error, only invalid choice we handle

        # Create a new model on the fly
        return self.queryset.model.objects.create(**{self.creation_field: value})
