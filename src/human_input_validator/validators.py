"""Pure validators for user-entered values.

Each function returns a normalized value or raises :class:`ValidationError`.
"""

from __future__ import annotations

import re
import urllib.parse
import pycountry


class ValidationError(ValueError):
    """Raised when a human-entered value cannot be validated."""


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")


def email(value: str) -> str:
    """Return a trimmed, lower-case email address."""
    normalized = value.strip().lower()
    if not _EMAIL_PATTERN.fullmatch(normalized):
        raise ValidationError("Enter a valid email address.")
    return normalized


def country(value: str) -> str:
    """Return the official name of an ISO 3166-1 country, given its name or code."""
    normalized = value.strip()
    try:
        result = pycountry.countries.lookup(normalized)
    except LookupError as error:
        raise ValidationError("Please enter a valid country") from error
    return result.name


def username(value: str, max_length: int = 12) -> str:
    """Checks a username length and allowed characters"""
    normalized = value.strip()
    if not _USERNAME_PATTERN.fullmatch(normalized):
        raise ValidationError("Enter a valid username.")
    if len(value) > max_length:
        raise ValidationError(f"Username can be max {max_length} letters long")

    return normalized.lower()


def phonenumber(value: str, pattern: str | list[str]) -> str:
    """Checks a phone number against one or more patterns, where '*' or '#' matches any digit."""
    normalized = value.strip()
    patterns = [pattern] if isinstance(pattern, str) else pattern
    if not any(_matches_phone_pattern(normalized, candidate) for candidate in patterns):
        raise ValidationError("Enter a valid phone number.")
    return normalized


def _matches_phone_pattern(value: str, pattern: str) -> bool:
    if len(value) != len(pattern):
        return False
    return all(v.isdigit() if p in "*#" else v == p for v, p in zip(value, pattern))


def creditcard(value: str) -> str:
    """Checks a creditcard number to be almost valid."""
    normalized = re.sub(r"[\s-]", "", value.strip())
    if not normalized.isdigit():
        raise ValidationError("Enter a valid creditcard number.")
    valid = False
    if len(normalized) >= 13 and len(normalized) <= 19:
        digits = [int(d) for d in reversed(normalized)]
        for i in range(1, len(digits), 2):
            digits[i] = digits[i] * 2 - 9 if digits[i] * 2 > 9 else digits[i] * 2
        valid = sum(digits) % 10 == 0

    if not valid:
        raise ValidationError("Enter a valid creditcard number.")
    return normalized


def name(value: str) -> str:
    """Return a trimmed name with each part capitalized."""
    normalized = value.strip()
    if not normalized.replace(" ", "").isalpha():
        raise ValidationError("Enter a valid name.")
    return " ".join(part.capitalize() for part in normalized.split())


def lastname(value: str) -> str:
    """Return a trimmed last name with each part capitalized."""
    normalized = value.strip()
    if not normalized.replace(" ", "").isalpha():
        raise ValidationError("Enter a valid last name.")
    return " ".join(part.capitalize() for part in normalized.split())


def is_valid_url(value: str) -> str:
    """Checks if the given value is a valid HTTP(S) URL."""

    normalized = value.strip()
    parsed = urllib.parse.urlparse(normalized)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("Enter a valid URL.")

    return normalized
