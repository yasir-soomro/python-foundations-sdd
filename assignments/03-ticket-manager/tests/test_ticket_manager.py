import io
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

ASSIGNMENT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ASSIGNMENT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cli import TicketCLI
from domain import Ticket, TicketStatus
from exceptions import TicketNotFoundError, ValidationError
from repository import InMemoryTicketRepository
from service import TicketService


class TicketTests(unittest.TestCase):
    def test_ticket_requires_valid_data(self) -> None:
        with self.assertRaises(ValidationError):
            Ticket("", "Fix login", "Investigate error")

        with self.assertRaises(ValidationError):
            Ticket("t-1", "   ", "Investigate error")

        with self.assertRaises(ValidationError):
            Ticket("t-1", "Fix login", "   ")

        with self.assertRaises(ValidationError):
            Ticket("t-1", "Fix login", "Investigate error", "Unknown")

    def test_new_ticket_starts_open(self) -> None:
        ticket = Ticket("t-1", "Fix login", "Investigate error")
        self.assertEqual(TicketStatus.OPEN, ticket.status)


class TicketServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryTicketRepository()
        self.service = TicketService(self.repository)

    def test_create_and_get_ticket(self) -> None:
        ticket = self.service.create_ticket("Fix login", "Investigate user session")

        self.assertTrue(ticket.ticket_id)
        self.assertEqual("Fix login", ticket.title)
        self.assertEqual("Investigate user session", ticket.description)
        self.assertEqual(TicketStatus.OPEN, ticket.status)
        self.assertEqual(ticket, self.service.get_ticket(ticket.ticket_id))

    def test_list_tickets_is_in_creation_order(self) -> None:
        first = self.service.create_ticket("First", "First description")
        second = self.service.create_ticket("Second", "Second description")

        tickets = self.service.list_tickets()

        self.assertEqual([first.ticket_id, second.ticket_id], [ticket.ticket_id for ticket in tickets])

    def test_update_ticket(self) -> None:
        ticket = self.service.create_ticket("Fix login", "Investigate user session")

        updated = self.service.update_ticket(ticket.ticket_id, "Fix authentication", "Review security logs")

        self.assertEqual("Fix authentication", updated.title)
        self.assertEqual("Review security logs", updated.description)
        self.assertEqual(ticket.ticket_id, updated.ticket_id)
        self.assertEqual(TicketStatus.OPEN, updated.status)

    def test_status_changes_follow_workflow(self) -> None:
        ticket = self.service.create_ticket("Fix login", "Investigate user session")

        self.service.change_status(ticket.ticket_id, TicketStatus.IN_PROGRESS)
        self.service.change_status(ticket.ticket_id, TicketStatus.RESOLVED)

        self.assertEqual(TicketStatus.RESOLVED, self.service.get_ticket(ticket.ticket_id).status)

        with self.assertRaises(ValidationError):
            self.service.change_status(ticket.ticket_id, TicketStatus.OPEN)

    def test_resolved_ticket_cannot_be_updated(self) -> None:
        ticket = self.service.create_ticket("Fix login", "Investigate user session")
        self.service.change_status(ticket.ticket_id, TicketStatus.RESOLVED)

        with self.assertRaises(ValidationError):
            self.service.update_ticket(ticket.ticket_id, "New title", "New description")

    def test_delete_ticket(self) -> None:
        ticket = self.service.create_ticket("Fix login", "Investigate user session")

        self.service.delete_ticket(ticket.ticket_id)

        self.assertEqual([], self.service.list_tickets())

    def test_invalid_values_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_ticket("   ", "Description")

        with self.assertRaises(ValidationError):
            self.service.create_ticket("Title", "   ")

    def test_missing_ticket_raises_not_found(self) -> None:
        with self.assertRaises(TicketNotFoundError):
            self.service.get_ticket("missing")

        with self.assertRaises(TicketNotFoundError):
            self.service.update_ticket("missing", "Title", "Description")

        with self.assertRaises(TicketNotFoundError):
            self.service.change_status("missing", TicketStatus.IN_PROGRESS)

        with self.assertRaises(TicketNotFoundError):
            self.service.update_ticket("missing", "Title", "Description")

        with self.assertRaises(TicketNotFoundError):
            self.service.change_status("missing", TicketStatus.IN_PROGRESS)

        with self.assertRaises(TicketNotFoundError):
            self.service.delete_ticket("missing")


class TicketCLITests(unittest.TestCase):
    def test_cli_creates_lists_and_changes_status(self) -> None:
        repository = InMemoryTicketRepository()
        ticket = repository.add(Ticket("t-1", "Fix login", "Investigate user session"))
        input_stream = io.StringIO(
            "2\n"
            "5\n"
            f"{ticket.ticket_id}\nIn Progress\n"
            "7\n"
        )
        output = io.StringIO()
        cli = TicketCLI(repository, input_stream, output)

        cli.run()

        output_text = output.getvalue()
        self.assertIn("Fix login", output_text)
        self.assertIn("Status changed", output_text)
        self.assertIn("Goodbye!", output_text)

    def test_cli_updates_and_deletes_ticket(self) -> None:
        repository = InMemoryTicketRepository()
        ticket = repository.add(Ticket("t-1", "Fix login", "Investigate user session"))
        input_stream = io.StringIO(
            f"4\n{ticket.ticket_id}\nFix authentication\nReview security logs\n"
            f"6\n{ticket.ticket_id}\n"
            "7\n"
        )
        output = io.StringIO()
        cli = TicketCLI(repository, input_stream, output)

        cli.run()

        output_text = output.getvalue()
        self.assertIn("Ticket updated", output_text)
        self.assertIn("Fix authentication", output_text)
        self.assertIn("Ticket deleted", output_text)
        self.assertEqual([], repository.list_all())

    def test_cli_reports_invalid_input_without_changing_data(self) -> None:
        repository = InMemoryTicketRepository()
        input_stream = io.StringIO(
            "1\n   \nInvestigate session\n"
            "7\n"
        )
        output = io.StringIO()
        cli = TicketCLI(repository, input_stream, output)

        cli.run()

        self.assertIn("Error:", output.getvalue())
        self.assertEqual([], repository.list_all())


if __name__ == "__main__":
    unittest.main()
