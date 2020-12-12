from fractions import Fraction

from django.test import TestCase

from . import fraction


class FractionTupleTestCase(TestCase):
    def test_as_tuple_error(self):
        case = Fraction("5/17")

        with self.assertRaises(ValueError):
            frac = fraction.as_fraction(case)
            prefix, nom, denom = fraction.as_tuple(frac)

    def test_tuple_without_prefix(self):
        case = Fraction("5/2")
        expected = (2, 1, 2)

        frac = fraction.as_fraction(case)
        parsed = fraction.as_tuple(frac)

        self.assertEqual(expected, parsed)

    def test_tuple_with_prefix(self):
        case = Fraction("1/2")
        expected = (None, 1, 2)

        frac = fraction.as_fraction(case)
        parsed = fraction.as_tuple(frac)

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
