"""Tests for humaninput validators."""

# pylint: disable=missing-class-docstring,missing-function-docstring
import unittest

from human_input_validator import (
    ValidationError,
    email,
    country,
    username,
    phonenumber,
    creditcard,
)


class EmailTests(unittest.TestCase):
    def test_normalizes_email(self) -> None:
        self.assertEqual(
            email("  Ada.Lovelace@Example.COM "), "ada.lovelace@example.com"
        )

    def test_rejects_invalid_email(self) -> None:
        with self.assertRaises(ValidationError):
            email("not-an-email")


class CountryTests(unittest.TestCase):
    def test_normalizes_country(self) -> None:
        self.assertEqual(country("SWEDEN "), "Sweden")

    def test_rejects_country(self) -> None:
        with self.assertRaises(ValidationError):
            country("Kolbäck")


class UsernameTests(unittest.TestCase):
    def test_normalizes_username(self) -> None:
        self.assertEqual(username("JohnDoe "), "johndoe")

    def test_rejects_username(self) -> None:
        with self.assertRaises(ValidationError):
            username("#my_name")


class PhonenumberTests(unittest.TestCase):
    def test_normalizes_phonenumber(self) -> None:
        self.assertEqual(
            phonenumber("0760000000", ["*#-*#*#*#*", "##########", "**********"]),
            "0760000000",
        )

    def test_rejects_phonenumber(self) -> None:
        with self.assertRaises(ValidationError):
            phonenumber("08-0000000", "***-*********")


class CreditcardTests(unittest.TestCase):
    def test_normalizes_creditcard(self) -> None:
        self.assertEqual(creditcard("0000-0000-0000-0000"), "0000000000000000")

    def test_rejects_creditcard(self) -> None:
        with self.assertRaises(ValidationError):
            creditcard("0123-4567-8901-2345")


if __name__ == "__main__":
    unittest.main()
