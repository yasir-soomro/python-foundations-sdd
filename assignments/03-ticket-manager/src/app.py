from __future__ import annotations

from cli import TicketCLI
from repository import InMemoryTicketRepository


class TicketManagerApp:
    """Creates the application components and starts the session."""

    def __init__(self) -> None:
        self._repository = InMemoryTicketRepository()
        self._cli = TicketCLI(self._repository, __import__("sys").stdin, __import__("sys").stdout)

    def run(self) -> None:
        self._cli.run()


if __name__ == "__main__":
    TicketManagerApp().run()
