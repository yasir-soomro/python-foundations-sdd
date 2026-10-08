from __future__ import annotations

from uuid import uuid4

from domain import Ticket, TicketStatus
from exceptions import RepositoryError, TicketNotFoundError, ValidationError
from repository import TicketRepository


class TicketService:
    """Business operations for tickets."""

    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository

    def create_ticket(self, title: str, description: str) -> Ticket:
        trimmed_title = title.strip()
        trimmed_description = description.strip()
        self._validate_title(trimmed_title)
        self._validate_description(trimmed_description)

        ticket = Ticket(
            ticket_id=str(uuid4()),
            title=trimmed_title,
            description=trimmed_description,
            status=TicketStatus.OPEN,
        )
        try:
            return self._repository.add(ticket)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        except Exception as exc:
            raise RepositoryError("Unable to create ticket.") from exc

    def get_ticket(self, ticket_id: str) -> Ticket:
        self._validate_ticket_id(ticket_id)
        try:
            return self._repository.get_by_id(ticket_id)
        except KeyError as exc:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to load ticket.") from exc

    def list_tickets(self) -> list[Ticket]:
        try:
            return self._repository.list_all()
        except Exception as exc:
            raise RepositoryError("Unable to list tickets.") from exc

    def update_ticket(self, ticket_id: str, title: str, description: str) -> Ticket:
        self._validate_ticket_id(ticket_id)
        existing = self.get_ticket(ticket_id)
        if existing.status is TicketStatus.RESOLVED:
            raise ValidationError("Resolved tickets cannot be updated.")

        trimmed_title = title.strip()
        trimmed_description = description.strip()
        self._validate_title(trimmed_title)
        self._validate_description(trimmed_description)

        updated = Ticket(
            ticket_id=existing.ticket_id,
            title=trimmed_title,
            description=trimmed_description,
            status=existing.status,
        )
        try:
            return self._repository.update(updated)
        except KeyError as exc:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to update ticket.") from exc

    def change_status(self, ticket_id: str, new_status: TicketStatus | str) -> Ticket:
        self._validate_ticket_id(ticket_id)
        ticket = self.get_ticket(ticket_id)
        normalized = new_status.value if isinstance(new_status, TicketStatus) else new_status.strip()
        status_order = {
            TicketStatus.OPEN: 0,
            TicketStatus.IN_PROGRESS: 1,
            TicketStatus.RESOLVED: 2,
        }
        if normalized not in TicketStatus.values():
            raise ValidationError("Ticket status must be Open, In Progress, or Resolved.")
        requested = TicketStatus(normalized)
        if status_order[requested] <= status_order[ticket.status]:
            raise ValidationError("Ticket status can only move forward through the workflow.")

        updated = Ticket(
            ticket_id=ticket.ticket_id,
            title=ticket.title,
            description=ticket.description,
            status=requested,
        )
        try:
            return self._repository.update(updated)
        except KeyError as exc:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to change ticket status.") from exc

    def delete_ticket(self, ticket_id: str) -> None:
        self._validate_ticket_id(ticket_id)
        self.get_ticket(ticket_id)
        try:
            self._repository.delete(ticket_id)
        except KeyError as exc:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' was not found.") from exc
        except Exception as exc:
            raise RepositoryError("Unable to delete ticket.") from exc

    @staticmethod
    def _validate_ticket_id(ticket_id: str) -> None:
        if not ticket_id.strip():
            raise ValidationError("Ticket ID is required.")

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title:
            raise ValidationError("Ticket title is required.")

    @staticmethod
    def _validate_description(description: str) -> None:
        if not description:
            raise ValidationError("Ticket description is required.")
