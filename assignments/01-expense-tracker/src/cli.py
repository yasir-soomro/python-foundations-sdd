from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import TextIO

from .domain import Expense
from .exceptions import ExpenseTrackerError
from .service import ExpenseService


class ExpenseCLI:
    """Terminal interface for the Expense Tracker."""

    def __init__(self, service: ExpenseService, input_stream: TextIO, output_stream: TextIO) -> None:
        self._service = service
        self._input = input_stream
        self._output = output_stream

    def run(self) -> None:
        self._output.write("Expense Tracker\n")
        while True:
            self._output.write("\n1. Add expense\n2. View expenses\n3. View total\n4. Filter by category\n5. Exit\nChoose an option: ")
            self._output.flush()
            choice = self._input.readline().strip()
            if not choice:
                self._output.write("Goodbye!\n")
                return

            try:
                if choice == "1":
                    self._add_expense()
                elif choice == "2":
                    self._view_expenses()
                elif choice == "3":
                    self._view_total()
                elif choice == "4":
                    self._filter_by_category()
                elif choice == "5":
                    self._output.write("Goodbye!\n")
                    return
                else:
                    self._output.write("Invalid option. Please choose 1-5.\n")
            except ExpenseTrackerError as exc:
                self._output.write(f"Error: {exc}\n")

    def _add_expense(self) -> None:
        description = self._prompt("Description: ")
        amount = self._prompt_decimal("Amount: ")
        category = self._prompt("Category: ")
        expense_date = self._prompt_date("Date (YYYY-MM-DD): ")

        expense = self._service.add_expense(
            description=f"{description} ({category})",
            amount=amount,
            date_value=expense_date,
        )
        self._output.write(f"Expense added: {self._format_expense(expense)}\n")

    def _view_expenses(self) -> None:
        expenses = self._service.list_expenses()
        if not expenses:
            self._output.write("No expenses found.\n")
            return
        for expense in expenses:
            self._output.write(f"- {self._format_expense(expense)}\n")

    def _view_total(self) -> None:
        self._output.write(f"Total: {self._service.get_total():,.2f}\n")

    def _filter_by_category(self) -> None:
        category = self._prompt("Category: ").strip()
        if not category:
            raise ValueError("Category is required.")
        expenses = self._service.filter_expenses(description=category)
        if not expenses:
            self._output.write("No expenses found for that category.\n")
            return
        for expense in expenses:
            self._output.write(f"- {self._format_expense(expense)}\n")

    def _prompt(self, message: str) -> str:
        self._output.write(message)
        self._output.flush()
        return self._input.readline().strip()

    def _prompt_decimal(self, message: str) -> Decimal:
        value = self._prompt(message)
        try:
            return Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("Amount must be a valid number.") from exc

    def _prompt_date(self, message: str) -> date:
        value = self._prompt(message)
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("Date must be in YYYY-MM-DD format.") from exc

    def _format_expense(self, expense: Expense) -> str:
        return (
            f"{expense.description} | {expense.amount:,.2f} | "
            f"{expense.date.isoformat()}"
        )


class InvalidOperation(ValueError):
    pass
