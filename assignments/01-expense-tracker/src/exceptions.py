class ExpenseTrackerError(Exception):
    """Base exception for Expense Tracker errors."""


class ValidationError(ExpenseTrackerError):
    """Raised when user-provided data is invalid."""


class ExpenseNotFoundError(ExpenseTrackerError):
    """Raised when an expense cannot be found."""


class RepositoryError(ExpenseTrackerError):
    """Raised when a repository operation cannot be completed."""
