# Ticket Manager Specification

## Problem

Small teams need a simple way to record, review, update, and close support or task tickets. The application must help maintain a clear current record without requiring a database or external service.

## Goal

Provide a small command-line application for managing tickets. Users can create tickets, inspect them, change their details or status, and delete them. All ticket data remains available only for the current application session.

## Ticket data

Each ticket contains:

- A unique generated ticket ID.
- A title that cannot be empty.
- A description that cannot be empty.
- A status with one of: Open, In Progress, Resolved.

## Required operations

1. Create a ticket.
2. List all tickets.
3. View one ticket by ID.
4. Update an existing ticket's title and description.
5. Change an existing ticket's status.
6. Delete an existing ticket.
7. Exit the application.

## Status workflow

```text
Open → In Progress → Resolved
```

Status changes may move forward only through this sequence. A ticket cannot move backward from Resolved to In Progress. A ticket may be updated while it is Open or In Progress. A resolved ticket may not be changed by the update operation.

## Validation and error handling

- Titles and descriptions must be non-empty after trimming whitespace.
- Status values must be one of the allowed values.
- Ticket IDs must identify an existing ticket.
- Invalid input must not change stored data.
- Missing tickets produce a clear not-found message.
- Invalid menu choices and invalid values return the user to the menu.

## Storage

The application uses in-memory storage only. Records exist only while the current application session runs.

## CLI behavior

```text
Ticket Manager

1. Create Ticket
2. List Tickets
3. View Ticket
4. Update Ticket
5. Change Status
6. Delete Ticket
7. Exit
```

The user may perform multiple operations during one session. Invalid selections and normal validation errors do not terminate the application.
