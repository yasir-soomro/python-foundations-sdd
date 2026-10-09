# Validation System Requirements

## Functional Requirements

- **VAL-01:** A validator accepts field names associated with one or more reusable validation rules.
- **VAL-02:** A required-field rule rejects `None`, empty strings, and strings containing only whitespace.
- **VAL-03:** A type rule accepts one expected type or a tuple of expected types and rejects values that do not match.
- **VAL-04:** An email rule accepts a string with a basic `local@domain.tld` structure and rejects malformed values.
- **VAL-05:** A positive-number rule accepts positive integers, floats, and `Decimal` values; it rejects booleans, non-numeric values, zero, negative, and non-finite numeric values.
- **VAL-06:** Validation collects all failures rather than stopping at the first failure.
- **VAL-07:** Every failure identifies its field and provides a readable message.
- **VAL-08:** Missing configured fields are checked as `None`; unconfigured input fields do not produce issues.

## Quality Requirements

- Use Python 3.12+ syntax and type hints.
- Keep the validation module independent of CLI, business, and persistence modules.
- Use only the Python standard library.
- Do not mutate caller-provided input or rule collections.
- Cover valid inputs, each invalid rule, aggregation, and relevant edge cases with `unittest`.
