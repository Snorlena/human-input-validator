"""Pure validators for user-entered values.

Each function returns a normalized value or raises :class:`ValidationError`.
"""

from __future__ import annotations

import difflib
import functools
import gettext
import os
import re
import urllib.parse
import pycountry


class ValidationError(ValueError):
    """Raised when a human-entered value cannot be validated."""


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")


@functools.lru_cache(maxsize=1)
def _localized_country_names() -> dict[str, str]:
    """Map lower-cased, translated country names (e.g. 'deutschland') to alpha-2 codes."""
    index: dict[str, str] = {}
    for locale in os.listdir(pycountry.LOCALES_DIR):
        try:
            translation = gettext.translation("iso3166-1", pycountry.LOCALES_DIR, languages=[locale])
        except FileNotFoundError:
            continue
        for entry in pycountry.countries:
            names = (
                entry.name,
                getattr(entry, "official_name", None),
                getattr(entry, "common_name", None),
            )
            for candidate in filter(None, names):
                translated = translation.gettext(candidate).strip().lower()
                index.setdefault(translated, entry.alpha_2)
    return index


def email(value: str) -> str:
    """Return a trimmed, lower-case email address."""
    normalized = value.strip().lower()
    if not _EMAIL_PATTERN.fullmatch(normalized):
        raise ValidationError("Enter a valid email address.")
    return normalized


_FUZZY_MATCH_CUTOFF = 0.8


def country(value: str) -> str:
    """Return the official name of an ISO 3166-1 country, given its name or code in any supported language."""
    normalized = value.strip()
    try:
        result = pycountry.countries.lookup(normalized)
        return result.name
    except LookupError:
        pass

    index = _localized_country_names()
    lowered = normalized.lower()
    alpha_2 = index.get(lowered)
    if alpha_2 is None:
        # Fall back to fuzzy matching for close spelling variants (e.g. hyphenation
        # or transliteration differences) not covered by the exact translation.
        close_matches = difflib.get_close_matches(lowered, index.keys(), n=1, cutoff=_FUZZY_MATCH_CUTOFF)
        if close_matches:
            alpha_2 = index[close_matches[0]]
    if alpha_2 is None:
        raise ValidationError("Please enter a valid country")
    result = pycountry.countries.get(alpha_2=alpha_2)
    if result is None:
        raise ValidationError("Please enter a valid country")
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
