import sys
import unittest
from decimal import Decimal
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.domain import Expense
from src.exceptions import ExpenseNotFoundError, ValidationError
from src.repository import InMemoryExpenseRepository
from src.service import ExpenseService


class ExpenseTests(unittest.TestCase):
    def test_expense_requires_valid_data(self) -> None:
        with self.assertRaises(ValidationError):
            Expense("", "Groceries", Decimal("10.00"), date(2026, 10, 8))

        with self.assertRaises(ValidationError):
            Expense("1", "Groceries", Decimal("0"), date(2026, 10, 8))

        with self.assertRaises(ValidationError):
            Expense("1", "Groceries", Decimal("10.00"), "2026-10-08")

    def test_expense_total_is_calculated_from_amounts(self) -> None:
        expenses = [
            Expense("1", "Rent", Decimal("900.00"), date(2026, 10, 1)),
            Expense("2", "Food", Decimal("45.50"), date(2026, 10, 2)),
        ]

        total = sum((expense.amount for expense in expenses), Decimal("0"))

        self.assertEqual(Decimal("945.50"), total)


class ExpenseServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryExpenseRepository()
        self.service = ExpenseService(self.repository)

    def test_add_and_get_expense(self) -> None:
        expense = self.service.add_expense(
            description="Groceries",
            amount=Decimal("24.99"),
            date=date(2026, 10, 8),
        )

        self.assertEqual("Groceries", expense.description)
        self.assertEqual(Decimal("24.99"), expense.amount)
        self.assertEqual(date(2026, 10, 8), expense.date)
        self.assertEqual(expense, self.service.get_expense(expense.expense_id))

    def test_list_expenses_is_sorted_by_date(self) -> None:
        self.service.add_expense("Food", Decimal("15.00"), date(2026, 10, 8))
        self.service.add_expense("Rent", Decimal("500.00"), date(2026, 10, 1))

        expenses = self.service.list_expenses()

        self.assertEqual(["Rent", "Food"], [expense.description for expense in expenses])

    def test_total_returns_sum_of_expenses(self) -> None:
        self.service.add_expense("Food", Decimal("15.00"), date(2026, 10, 8))
        self.service.add_expense("Transport", Decimal("10.50"), date(2026, 10, 7))

        self.assertEqual(Decimal("25.50"), self.service.get_total())

    def test_filter_expenses_by_description(self) -> None:
        self.service.add_expense("Groceries", Decimal("20.00"), date(2026, 10, 8))
        self.service.add_expense("Transport", Decimal("10.00"), date(2026, 10, 9))

        filtered = self.service.filter_expenses(description="grocer")

        self.assertEqual(1, len(filtered))
        self.assertEqual("Groceries", filtered[0].description)

    def test_filter_expenses_by_date(self) -> None:
        self.service.add_expense("Rent", Decimal("500.00"), date(2026, 10, 1))
        self.service.add_expense("Food", Decimal("20.00"), date(2026, 10, 8))

        filtered = self.service.filter_expenses(date_value=date(2026, 10, 8))

        self.assertEqual(["Food"], [expense.description for expense in filtered])

    def test_update_expense(self) -> None:
        expense = self.service.add_expense("Food", Decimal("20.00"), date(2026, 10, 8))

        updated = self.service.update_expense(
            expense.expense_id,
            description="Groceries",
            amount=Decimal("25.50"),
            date=date(2026, 10, 9),
        )

        self.assertEqual("Groceries", updated.description)
        self.assertEqual(Decimal("25.50"), updated.amount)
        self.assertEqual(date(2026, 10, 9), updated.date)

    def test_delete_expense(self) -> None:
        expense = self.service.add_expense("Food", Decimal("20.00"), date(2026, 10, 8))

        self.service.delete_expense(expense.expense_id)

        self.assertEqual([], self.service.list_expenses())

    def test_invalid_description_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.add_expense("   ", Decimal("10.00"), date(2026, 10, 8))

    def test_invalid_amount_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.add_expense("Food", Decimal("0"), date(2026, 10, 8))

        with self.assertRaises(ValidationError):
            self.service.add_expense("Food", Decimal("-1.00"), date(2026, 10, 8))

    def test_missing_expense_raises_not_found(self) -> None:
        with self.assertRaises(ExpenseNotFoundError):
            self.service.get_expense("missing")

        with self.assertRaises(ExpenseNotFoundError):
            self.service.update_expense("missing", "Food", Decimal("10.00"), date(2026, 10, 8))

        with self.assertRaises(ExpenseNotFoundError):
            self.service.delete_expense("missing")

    def test_filter_requires_value(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.filter_expenses(description="   ")

        with self.assertRaises(ValidationError):
            self.service.filter_expenses(date_value=None)


if __name__ == "__main__":
    unittest.main()
