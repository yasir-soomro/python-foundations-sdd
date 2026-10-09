# Validation System Specification

## Purpose

Provide a small, reusable validation component for checking mapping-based input. It must be usable by different applications without depending on their CLI, domain, or persistence code.

## Behavior

- A caller configures a `Validator` with an ordered mapping of field names to validation rules.
- Supported rules check required values, runtime types, basic email-address structure, and positive numeric values.
- Required values are not `None` or blank/whitespace-only strings.
- Each configured rule runs for its field. Validation does not stop at the first failure.
- The result is an ordered list of field-specific issues. Each issue contains the field name and a clear message.
- A missing mapping key is validated as `None`; unrelated input keys are ignored.
- Validation does not modify the input mapping or its values.

## Scope

This assignment provides validation primitives only. It does not define application-specific schemas, CLI behavior, error presentation, data conversion, or external integrations. Email validation checks a practical basic structure; it does not claim full standards compliance or verify deliverability.
