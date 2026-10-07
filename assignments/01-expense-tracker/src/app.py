from __future__ import annotations

from io import StringIO

from .cli import ExpenseCLI
from .repository import InMemoryExpenseRepository
from .service import ExpenseService


class ExpenseTrackerApp:
    """Application lifecycle coordinator."""

    def __init__(self, input_stream: StringIO | None = None, output_stream: StringIO | None = None) -> None:
        self._input = input_stream if input_stream is not None else StringIO("5\n")
        self._output = output_stream if output_stream is not None else StringIO()

    def run(self) -> str:
        repository = InMemoryExpenseRepository()
        service = ExpenseService(repository)
        cli = ExpenseCLI(service, self._input, self._output)
        cli.run()
        return self._output.getvalue()


if __name__ == "__main__":
    import sys

    app = ExpenseTrackerApp(sys.stdin, sys.stdout)
    app.run()
