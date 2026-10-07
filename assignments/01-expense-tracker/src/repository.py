from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import Iterable

from .domain import Expense


class ExpenseRepository(ABC):
    """Persistence contract for expense records."""

    @abstractmethod
    def add(self, expense: Expense) -> Expense:
        """Store a new expense and return it."""

    @abstractmethod
    def get_by_id(self, expense_id: str) -> Expense:
        """Return the expense with the given identifier."""

    @abstractmethod
    def list_all(self) -> list[Expense]:
        """Return all expenses."""

    @abstractmethod
    def update(self, expense: Expense) -> Expense:
        """Replace an existing expense."""

    @abstractmethod
    def delete(self, expense_id: str) -> None:
        """Delete an expense."""

    @abstractmethod
    def filter_by_description(self, value: str) -> list[Expense]:
        """Return expenses whose description contains the value."""

    @abstractmethod
    def filter_by_date(self, value: date) -> list[Expense]:
        """Return expenses recorded on the given date."""


class InMemoryExpenseRepository(ExpenseRepository):
    """Simple in-memory repository used by this assignment."""

    def __init__(self) -> None:
        self._expenses: dict[str, Expense] = {}

    def add(self, expense: Expense) -> Expense:
        if expense.expense_id in self._expenses:
            raise ValueError(f"Expense with ID '{expense.expense_id}' already exists.")
        self._expenses[expense.expense_id] = expense
        return expense

    def get_by_id(self, expense_id: str) -> Expense:
        try:
            return self._expenses[expense_id]
        except KeyError as exc:
            raise KeyError(f"Expense '{expense_id}' does not exist.") from exc

    def list_all(self) -> list[Expense]:
        return sorted(self._expenses.values(), key=lambda expense: expense.date)

    def update(self, expense: Expense) -> Expense:
        if expense.expense_id not in self._expenses:
            raise KeyError(f"Expense '{expense.expense_id}' does not exist.")
        self._expenses[expense.expense_id] = expense
        return expense

    def delete(self, expense_id: str) -> None:
        if expense_id not in self._expenses:
            raise KeyError(f"Expense '{expense_id}' does not exist.")
        del self._expenses[expense_id]

    def filter_by_description(self, value: str) -> list[Expense]:
        normalized = value.casefold()
        return [
            expense for expense in self.list_all()
            if normalized in expense.description.casefold()
        ]

    def filter_by_date(self, value: date) -> list[Expense]:
        return [expense for expense in self.list_all() if expense.date == value]
