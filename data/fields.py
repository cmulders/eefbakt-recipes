from decimal import Decimal

from django import forms
from django.utils.translation import gettext_lazy as _
from utils import fraction


class FractionField(forms.DecimalField):
    widget = forms.widgets.Input

    default_error_messages = {
        "invalid": _("Enter a number or a fraction."),
    }

    def prepare_value(self, value):
        try:
            return fraction.format_fraction(value)
        except ValueError:
            return super().prepare_value(value)

    def to_python(self, value):
        """
        Check if the input is a fraction and pass a Decimal to the underlying to_python function of Decumal.
        """
        if value in self.empty_values:
            return None

        value = value.replace(",", ".")  # force dot sep

        try:
            value = fraction.parse_fraction(value)
            value = Decimal(value.numerator) / Decimal(value.denominator)
            value = f"{value:{self.max_digits}.{self.decimal_places}f}"
        except ValueError:
            pass

        return super().to_python(value)
