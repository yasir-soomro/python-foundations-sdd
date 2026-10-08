from __future__ import annotations

from abc import ABC, abstractmethod

from domain import Ticket


class TicketRepository(ABC):
    """Persistence contract for tickets."""

    @abstractmethod
    def add(self, ticket: Ticket) -> Ticket:
        """Store a new ticket."""

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Ticket:
        """Return a ticket by identifier."""

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        """Return all tickets."""

    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket:
        """Replace a ticket."""

    @abstractmethod
    def delete(self, ticket_id: str) -> None:
        """Delete a ticket."""


class InMemoryTicketRepository(TicketRepository):
    """In-memory storage for tickets."""

    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}

    def add(self, ticket: Ticket) -> Ticket:
        if ticket.ticket_id in self._tickets:
            raise ValueError(f"Ticket with ID '{ticket.ticket_id}' already exists.")
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> Ticket:
        try:
            return self._tickets[ticket_id]
        except KeyError as exc:
            raise KeyError(f"Ticket '{ticket_id}' does not exist.") from exc

    def list_all(self) -> list[Ticket]:
        return list(self._tickets.values())

    def update(self, ticket: Ticket) -> Ticket:
        if ticket.ticket_id not in self._tickets:
            raise KeyError(f"Ticket '{ticket.ticket_id}' does not exist.")
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def delete(self, ticket_id: str) -> None:
        if ticket_id not in self._tickets:
            raise KeyError(f"Ticket '{ticket_id}' does not exist.")
        del self._tickets[ticket_id]
