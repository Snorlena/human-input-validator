# Human-input-validator

`Human-input-validator` validates and normalizes common data entered by people. It
provides validators for email addresses, countries, usernames, phone
numbers, names, and credit card numbers.

```python
from human_input_validator import (
  email,
  country,
  username,
  phonenumber,
  creditcard,
  name,
  lastname,
)

customer_email = email("Ada.Lovelace@Example.COM")
customer_country = country("SWEDEN ")
customer_username = username("JohnDoe ")
customer_phone = phonenumber("08-0000000", "**-*******")
customer_card = creditcard("4111 1111 1111 1111")
customer_name = name("ada lovelace")
customer_lastname = lastname("lovelace")
```

Each function returns a normalized value or raises `ValidationError` for
invalid input.

- `email(value)` — returns a trimmed, lower-cased email address.
- `country(value)` — returns the official ISO 3166-1 country name, given a
  name or code.
- `username(value, max_length=12)` — returns a lower-cased username, checking
  length and allowed characters.
- `phonenumber(value, pattern)` — checks a phone number against one or more
  masks, where `*` or `#` matches any digit and other characters must match
  literally. `pattern` accepts a single mask or a list of masks.
- `creditcard(value)` — checks a credit card number's length and Luhn
  checksum, ignoring spaces and dashes.
- `name(value)` — returns a trimmed, capitalized name.
- `lastname(value)` — returns a trimmed, capitalized last name.

## Development

Run the test suite without installing the package:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
