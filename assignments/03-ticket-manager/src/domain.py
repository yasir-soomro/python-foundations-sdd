from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from exceptions import ValidationError


class TicketStatus(str, Enum):
    """Allowed ticket statuses."""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]


@dataclass(frozen=True)
class Ticket:
    """A support or task ticket."""

    ticket_id: str
    title: str
    description: str
    status: TicketStatus | str = TicketStatus.OPEN

    def __post_init__(self) -> None:
        ticket_id = self.ticket_id.strip()
        title = self.title.strip()
        description = self.description.strip()
        status = self.status.value if isinstance(self.status, TicketStatus) else self.status.strip()

        if not ticket_id:
            raise ValidationError("Ticket ID is required.")
        if not title:
            raise ValidationError("Ticket title is required.")
        if not description:
            raise ValidationError("Ticket description is required.")
        if status not in TicketStatus.values():
            raise ValidationError("Ticket status must be Open, In Progress, or Resolved.")

        object.__setattr__(self, "ticket_id", ticket_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "description", description)
        object.__setattr__(self, "status", TicketStatus(status))
