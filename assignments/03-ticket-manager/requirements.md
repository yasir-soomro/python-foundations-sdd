# Ticket Manager Requirements

## Functional requirements

1. The application shall allow a user to create a ticket with a title and description.
2. The application shall generate a unique ticket identifier automatically.
3. The application shall assign a new ticket the status `Open`.
4. The application shall list all stored tickets.
5. The application shall allow a user to view one ticket by identifier.
6. The application shall allow a user to update an existing ticket's title and description.
7. The application shall allow a user to change an existing ticket's status.
8. The application shall allow a user to delete an existing ticket by identifier.
9. When no tickets exist, the application shall display an empty-state message.

## Validation requirements

1. Ticket titles shall be non-empty after trimming whitespace.
2. Ticket descriptions shall be non-empty after trimming whitespace.
3. Ticket statuses shall be one of `Open`, `In Progress`, or `Resolved`.
4. Ticket identifiers shall be non-empty when required.
5. Updating a resolved ticket shall be rejected.
6. Status transitions shall only move forward through `Open`, `In Progress`, and `Resolved`.
7. Invalid input shall not change stored data.

## Error-handling requirements

1. Validation failures shall raise a domain-specific validation error.
2. Missing tickets shall raise a domain-specific not-found error.
3. Repository failures shall propagate as exceptions rather than being silently ignored.
4. CLI errors shall display a user-readable message and return to the menu.
5. Unexpected exceptions shall be reported without exposing internal implementation details.

## CLI requirements

1. The CLI shall provide a menu with options for creating, listing, viewing, updating, status changes, deleting, and exiting.
2. The CLI shall read input through standard input and write output through standard output.
3. The CLI shall display clear results after each operation.
4. The CLI shall return to the menu after a completed operation unless the user exits.
5. The CLI shall continue accepting commands after normal validation and not-found errors.

## Non-functional requirements

1. The application shall use Python 3.12 or newer.
2. The application shall use type hints for public interfaces.
3. The application shall use object-oriented design with small, focused responsibilities.
4. Business logic shall remain independent of CLI input and output.
5. Persistence shall use an in-memory repository for the current assignment.
6. The application shall use only the Python standard library.
