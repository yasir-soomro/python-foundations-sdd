from __future__ import annotations

from typing import TextIO

from domain import Ticket, TicketStatus
from exceptions import TicketManagerError
from repository import TicketRepository
from service import TicketService


class TicketCLI:
    """Terminal interface for the Ticket Manager."""

    def __init__(
        self,
        repository: TicketRepository,
        input_stream: TextIO,
        output_stream: TextIO,
    ) -> None:
        self._service = TicketService(repository)
        self._input = input_stream
        self._output = output_stream

    def run(self) -> None:
        self._output.write("Ticket Manager\n")
        while True:
            self._output.write(
                "\n1. Create Ticket\n"
                "2. List Tickets\n"
                "3. View Ticket\n"
                "4. Update Ticket\n"
                "5. Change Status\n"
                "6. Delete Ticket\n"
                "7. Exit\n"
                "Choose an option: "
            )
            self._output.flush()
            choice = self._input.readline()
            if not choice:
                self._output.write("Goodbye!\n")
                return

            choice = choice.strip()
            try:
                if choice == "1":
                    self._create_ticket()
                elif choice == "2":
                    self._list_tickets()
                elif choice == "3":
                    self._view_ticket()
                elif choice == "4":
                    self._update_ticket()
                elif choice == "5":
                    self._change_status()
                elif choice == "6":
                    self._delete_ticket()
                elif choice == "7":
                    self._output.write("Goodbye!\n")
                    return
                else:
                    self._output.write("Invalid option. Please choose 1-7.\n")
            except TicketManagerError as exc:
                self._output.write(f"Error: {exc}\n")

    def _create_ticket(self) -> None:
        ticket = self._service.create_ticket(
            self._prompt("Title: "),
            self._prompt("Description: "),
        )
        self._output.write(f"Ticket created: {self._format_ticket(ticket)}\n")

    def _list_tickets(self) -> None:
        tickets = self._service.list_tickets()
        if not tickets:
            self._output.write("No tickets found.\n")
            return
        self._output.write("Tickets:\n")
        for ticket in tickets:
            self._output.write(f"- {self._format_ticket(ticket)}\n")

    def _view_ticket(self) -> None:
        ticket = self._service.get_ticket(self._prompt("Ticket ID: "))
        self._output.write(f"Ticket: {self._format_ticket(ticket)}\n")

    def _update_ticket(self) -> None:
        ticket_id = self._prompt("Ticket ID: ")
        ticket = self._service.update_ticket(
            ticket_id,
            self._prompt("Title: "),
            self._prompt("Description: "),
        )
        self._output.write(f"Ticket updated: {self._format_ticket(ticket)}\n")

    def _change_status(self) -> None:
        ticket_id = self._prompt("Ticket ID: ")
        status = self._prompt("New status (Open, In Progress, Resolved): ")
        ticket = self._service.change_status(ticket_id, status)
        self._output.write(f"Status changed: {self._format_ticket(ticket)}\n")

    def _delete_ticket(self) -> None:
        ticket_id = self._prompt("Ticket ID: ")
        self._service.delete_ticket(ticket_id)
        self._output.write(f"Ticket deleted: {ticket_id}\n")

    def _prompt(self, message: str) -> str:
        self._output.write(message)
        self._output.flush()
        return self._input.readline().strip()

    @staticmethod
    def _format_ticket(ticket: Ticket) -> str:
        return f"{ticket.ticket_id} | {ticket.title} | {ticket.description} | {ticket.status.value}"


if __name__ == "__main__":
    from app import TicketManagerApp

    TicketManagerApp().run()
