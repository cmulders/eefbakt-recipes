from fractions import Fraction

from django.test import TestCase

from . import fraction


class FormatFractionTestCase(TestCase):
    def test_format_precision_error(self):
        case = Fraction("5/17")
        expected = "2 1/2"
        with self.assertRaises(ValueError):
            parsed = fraction.format_fraction(case)

    def test_format_without_prefix(self):
        case = Fraction("5/2")
        expected = "2 1/2"
        parsed = fraction.format_fraction(case)

        self.assertEqual(expected, parsed)

    def test_pformatwith_prefix(self):
        case = Fraction("1/2")
        expected = "1/2"
        parsed = fraction.format_fraction(case)

        self.assertEqual(expected, parsed)


class ParseFractionTestCase(TestCase):
    def test_parse_without_prefix(self):
        case = "5/2"
        expected = Fraction("5/2")
        parsed = fraction.parse_fraction(case)

        self.assertEqual(expected, parsed)

    def test_parse_with_prefix(self):
        case = "2 1/2"
        expected = Fraction("5/2")
        parsed = fraction.parse_fraction(case)

        self.assertEqual(expected, parsed)
