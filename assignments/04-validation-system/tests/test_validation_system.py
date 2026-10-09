import sys
import unittest
from decimal import Decimal
from pathlib import Path

ASSIGNMENT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ASSIGNMENT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from validation import (
    EmailRule,
    PositiveNumberRule,
    RequiredRule,
    TypeRule,
    ValidationIssue,
    Validator,
)


class ValidationRuleTests(unittest.TestCase):
    def test_required_rule_accepts_nonblank_values(self) -> None:
        rule = RequiredRule()

        self.assertIsNone(rule.validate("name", "Ada"))
        self.assertIsNone(rule.validate("count", 0))

    def test_required_rule_rejects_missing_and_blank_values(self) -> None:
        rule = RequiredRule()

        for value in (None, "", " \t\n"):
            with self.subTest(value=value):
                self.assertEqual("name is required.", rule.validate("name", value))

    def test_type_rule_accepts_one_or_multiple_types(self) -> None:
        self.assertIsNone(TypeRule(str).validate("name", "Ada"))
        self.assertIsNone(TypeRule((int, float)).validate("amount", 1.5))

    def test_type_rule_reports_expected_type(self) -> None:
        issue = TypeRule(str).validate("name", 42)

        self.assertEqual("name must be of type str.", issue)

    def test_email_rule_accepts_basic_address_structure(self) -> None:
        self.assertIsNone(EmailRule().validate("email", "ada@example.com"))

    def test_email_rule_rejects_malformed_values(self) -> None:
        for value in ("", "missing-at.example.com", "ada@localhost", "ada @example.com", 42):
            with self.subTest(value=value):
                self.assertEqual(
                    "email must be a valid email address.",
                    EmailRule().validate("email", value),
                )

    def test_positive_number_rule_accepts_positive_numeric_types(self) -> None:
        rule = PositiveNumberRule()

        for value in (1, 0.25, Decimal("10.5")):
            with self.subTest(value=value):
                self.assertIsNone(rule.validate("amount", value))

    def test_positive_number_rule_rejects_invalid_and_non_finite_values(self) -> None:
        rule = PositiveNumberRule()

        for value in (0, -1, True, "2", float("inf"), float("nan"), Decimal("NaN")):
            with self.subTest(value=value):
                self.assertEqual(
                    "amount must be a positive number.",
                    rule.validate("amount", value),
                )


class ValidatorTests(unittest.TestCase):
    def test_valid_input_returns_no_issues(self) -> None:
        validator = Validator(
            {
                "name": [RequiredRule(), TypeRule(str)],
                "email": [RequiredRule(), EmailRule()],
                "amount": [PositiveNumberRule()],
            }
        )

        issues = validator.validate(
            {"name": "Ada", "email": "ada@example.com", "amount": Decimal("3.50")}
        )

        self.assertEqual([], issues)

    def test_collects_all_field_and_rule_issues_in_order(self) -> None:
        validator = Validator(
            {
                "name": [RequiredRule(), TypeRule(str)],
                "email": [EmailRule()],
                "amount": [PositiveNumberRule()],
            }
        )

        issues = validator.validate({"name": " ", "email": "bad", "amount": 0})

        self.assertEqual(
            [
                ValidationIssue("name", "name is required."),
                ValidationIssue("email", "email must be a valid email address."),
                ValidationIssue("amount", "amount must be a positive number."),
            ],
            issues,
        )

    def test_missing_fields_are_validated_and_unconfigured_fields_ignored(self) -> None:
        validator = Validator({"name": [RequiredRule()]})

        issues = validator.validate({"extra": "ignored"})

        self.assertEqual([ValidationIssue("name", "name is required.")], issues)

    def test_rules_and_values_are_not_modified(self) -> None:
        field_rules = [RequiredRule()]
        rules = {"name": field_rules}
        values = {"name": "Ada"}
        validator = Validator(rules)

        field_rules.clear()
        issues = validator.validate(values)

        self.assertEqual([], issues)
        self.assertEqual({"name": "Ada"}, values)


if __name__ == "__main__":
    unittest.main()