from django import forms
from django.forms.formsets import ORDERING_FIELD_NAME


class OrderFirstInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        if self.can_order:
            # Make the Ordering field the first,
            form.order_fields([ORDERING_FIELD_NAME])
