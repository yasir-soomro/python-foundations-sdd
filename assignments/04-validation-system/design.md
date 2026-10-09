# Validation System Design

## Module

`src/validation.py` owns the reusable validation API. It has no dependencies on application or infrastructure layers.

## Types and Responsibilities

- `ValidationRule` is a protocol for a rule that checks a field/value pair and returns either a message or `None`.
- `RequiredRule`, `TypeRule`, `EmailRule`, and `PositiveNumberRule` implement independent, reusable checks.
- `ValidationIssue` is an immutable field/message result.
- `Validator` stores an ordered, defensive copy of each field's rules. Its `validate` method runs every rule and returns all issues in field and rule order.

## Validation Flow

The caller constructs a `Validator` with a mapping from field names to rule sequences, then passes an input mapping to `validate`. For each configured field, the validator obtains its value (using `None` when absent), applies every rule, and appends each returned message as a `ValidationIssue`. The caller decides how to present or act on the result.

## Error and Boundary Decisions

- Rules return messages instead of raising for ordinary invalid input, allowing aggregation.
- Type checks use `isinstance`; numeric validation explicitly excludes `bool`, despite it being an `int` subclass.
- Email validation uses a small standard-library pattern for common address structure, not full RFC validation.
- Positive-number validation supports `int`, `float`, and `Decimal`, and rejects non-finite floats and decimals.
- No CLI, application service, domain model, repository, or third-party dependency is introduced.
