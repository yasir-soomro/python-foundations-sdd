# Expense Tracker Requirements

## Functional requirements

1. The application shall allow a user to add an expense with a description, amount, and date.
2. The application shall display all saved expenses in chronological order.
3. The application shall calculate and display the total of all saved expenses.
4. The application shall allow a user to filter expenses by date or description.
5. The application shall allow a user to remove an expense.
6. The application shall allow a user to update an existing expense.
7. When no expenses exist, the application shall display an empty-state message.

## Non-functional requirements

1. The application shall use Python 3.12 or newer.
2. The application shall use type hints for public interfaces.
3. The application shall use object-oriented design with small, focused responsibilities.
4. Business logic shall be independent of CLI input and output.
5. Persistence shall use an in-memory repository for the current assignment.
6. Core business operations shall be reusable by a future FastAPI layer.
7. The application shall use only the Python standard library.

## CLI requirements

1. The CLI shall provide a menu with options for adding, viewing, updating, removing, filtering, showing totals, and exiting.
2. The CLI shall read user input through standard input.
3. The CLI shall display clear results after each operation.
4. The CLI shall return to the menu after completing an operation unless the user exits.
5. The CLI shall display a clear message when an operation is not available or cannot be completed.

## Validation requirements

1. Expense descriptions shall be non-empty after trimming whitespace.
2. Expense amounts shall be greater than zero.
3. Expense dates shall be valid ISO dates.
4. Updating or removing an expense shall require an existing expense identifier.
5. Filtering shall accept a non-empty date or description value.
6. Invalid user input shall not change stored data.

## Error-handling requirements

1. Validation failures shall raise a domain-specific validation error.
2. Missing expenses shall raise a domain-specific not-found error.
3. Repository failures shall propagate as exceptions rather than being silently ignored.
4. CLI errors shall display a user-readable message and return to the menu.
5. Unexpected exceptions shall be reported without exposing internal implementation details.

## Future FastAPI compatibility requirements

1. Application services shall expose operations independent of CLI types and console I/O.
2. Repository contracts shall be independent of the in-memory implementation.
3. Domain entities shall not depend on web frameworks or request models.
4. A future API layer shall be able to call the same service methods with typed request data.
5. CLI-specific formatting shall remain outside the reusable business layer.
