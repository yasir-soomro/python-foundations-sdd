from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .exceptions import ValidationError


@dataclass(frozen=True)
class Expense:
    """A single expense record."""

    expense_id: str
    description: str
    amount: Decimal
    date: date

    def __post_init__(self) -> None:
        if not isinstance(self.expense_id, str) or not self.expense_id.strip():
            raise ValidationError("Expense ID is required.")
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValidationError("Expense description is required.")
        if not isinstance(self.amount, Decimal) or self.amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")
        if not isinstance(self.date, date):
            raise ValidationError("Expense date must be a valid date.")
