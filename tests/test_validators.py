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
    name,
    lastname,
    is_valid_url,
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


class NameTests(unittest.TestCase):
    def test_normalizes_name(self) -> None:
        self.assertEqual(name("  ada lovelace "), "Ada Lovelace")

    def test_rejects_name(self) -> None:
        with self.assertRaises(ValidationError):
            name("Ada123") 


class LastnameTests(unittest.TestCase):
    def test_normalizes_lastname(self) -> None:
        self.assertEqual(lastname("  lovelace "), "Lovelace")

    def test_rejects_lastname(self) -> None:
        with self.assertRaises(ValidationError):
            lastname("Lovelace123")


class IsValidUrlTests(unittest.TestCase):
    def test_normalizes_url(self) -> None:
        self.assertEqual(is_valid_url("  https://example.com "), "https://example.com")

    def test_rejects_invalid_url(self) -> None:
        with self.assertRaises(ValidationError):
            is_valid_url("not-a-url")


if __name__ == "__main__":
    unittest.main()
