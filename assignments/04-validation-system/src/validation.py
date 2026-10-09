from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


class ValidationRule(Protocol):
    def validate(self, field: str, value: object) -> str | None:
        """Return an error message when the value is invalid."""


@dataclass(frozen=True)
class RequiredRule:
    def validate(self, field: str, value: object) -> str | None:
        if value is None or (isinstance(value, str) and not value.strip()):
            return f"{field} is required."
        return None


@dataclass(frozen=True)
class TypeRule:
    expected_type: type | tuple[type, ...]

    def validate(self, field: str, value: object) -> str | None:
        if isinstance(value, self.expected_type):
            return None

        expected_types = (
            self.expected_type
            if isinstance(self.expected_type, tuple)
            else (self.expected_type,)
        )
        expected = " or ".join(expected_type.__name__ for expected_type in expected_types)
        return f"{field} must be of type {expected}."


@dataclass(frozen=True)
class EmailRule:
    _pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    def validate(self, field: str, value: object) -> str | None:
        if isinstance(value, str) and self._pattern.fullmatch(value):
            return None
        return f"{field} must be a valid email address."


@dataclass(frozen=True)
class PositiveNumberRule:
    def validate(self, field: str, value: object) -> str | None:
        if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
            return f"{field} must be a positive number."

        if isinstance(value, float):
            is_positive = math.isfinite(value) and value > 0
        elif isinstance(value, Decimal):
            is_positive = value.is_finite() and value > 0
        else:
            is_positive = value > 0

        if not is_positive:
            return f"{field} must be a positive number."
        return None


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


class Validator:
    def __init__(self, rules: Mapping[str, Sequence[ValidationRule]]) -> None:
        self._rules = {field: tuple(field_rules) for field, field_rules in rules.items()}

    def validate(self, values: Mapping[str, object]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for field, field_rules in self._rules.items():
            value = values.get(field)
            for rule in field_rules:
                message = rule.validate(field, value)
                if message is not None:
                    issues.append(ValidationIssue(field, message))
        return issues