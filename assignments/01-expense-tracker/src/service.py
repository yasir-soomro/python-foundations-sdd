from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal
from uuid import uuid4

from .domain import Expense
from .exceptions import ExpenseNotFoundError, RepositoryError, ValidationError
from .repository import ExpenseRepository


class ExpenseService:
    """Business operations for managing expenses."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self._repository = repository

    def add_expense(
        self,
        description: str,
        amount: Decimal,
        date: date_type,
    ) -> Expense:
        description = description.strip()
        if not description:
            raise ValidationError("Expense description is required.")
        if amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")
        if not isinstance(date, date_type):
            raise ValidationError("Expense date must be a valid date.")

        expense = Expense(
            expense_id=str(uuid4()),
            description=description,
            amount=amount,
            date=date,
        )
        try:
            return self._repository.add(expense)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        except Exception as exc:
            raise RepositoryError("Unable to add expense.") from exc

    def get_expense(self, expense_id: str) -> Expense:
        try:
            return self._repository.get_by_id(expense_id)
        except KeyError as exc:
            raise ExpenseNotFoundError(f"Expense '{expense_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to load expense.") from exc

    def list_expenses(self) -> list[Expense]:
        try:
            return self._repository.list_all()
        except Exception as exc:
            raise RepositoryError("Unable to list expenses.") from exc

    def update_expense(
        self,
        expense_id: str,
        description: str,
        amount: Decimal,
        date: date_type,
    ) -> Expense:
        existing = self.get_expense(expense_id)
        description = description.strip()
        if not description:
            raise ValidationError("Expense description is required.")
        if amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")
        if not isinstance(date, date_type):
            raise ValidationError("Expense date must be a valid date.")

        updated = Expense(
            expense_id=existing.expense_id,
            description=description,
            amount=amount,
            date=date,
        )
        try:
            return self._repository.update(updated)
        except KeyError as exc:
            raise ExpenseNotFoundError(f"Expense '{expense_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to update expense.") from exc

    def delete_expense(self, expense_id: str) -> None:
        self.get_expense(expense_id)
        try:
            self._repository.delete(expense_id)
        except KeyError as exc:
            raise ExpenseNotFoundError(f"Expense '{expense_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to delete expense.") from exc

    def get_total(self) -> Decimal:
        return sum((expense.amount for expense in self.list_expenses()), Decimal("0"))

    def filter_expenses(
        self,
        description: str | None = None,
        date_value: date | None = None,
    ) -> list[Expense]:
        if description is not None and not description.strip():
            raise ValidationError("Filter value is required.")
        if date_value is not None and not isinstance(date_value, date_type):
            raise ValidationError("Filter date must be a valid date.")
        if description is None and date_value is None:
            raise ValidationError("A filter value is required.")

        try:
            if description is not None:
                return self._repository.filter_by_description(description)
            if date_value is not None:
                return self._repository.filter_by_date(date_value)
            return self.list_expenses()
        except Exception as exc:
            raise RepositoryError("Unable to filter expenses.") from exc

