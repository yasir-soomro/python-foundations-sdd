class TicketManagerError(Exception):
    """Base exception for Ticket Manager errors."""


class ValidationError(TicketManagerError):
    """Raised when ticket data is invalid."""


class TicketNotFoundError(TicketManagerError):
    """Raised when a ticket cannot be found."""


class RepositoryError(TicketManagerError):
    """Raised when a repository operation cannot be completed."""
