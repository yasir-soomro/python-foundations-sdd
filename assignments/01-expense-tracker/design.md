# Expense Tracker Design

## Architecture

The application uses a four-layer design:

```text
CLI layer
    ↓
Application service layer
    ↓
Domain layer
    ↓
Repository/data layer
```

The CLI depends on application services. The service depends on the domain model and repository interface. The in-memory repository implements the repository contract.

## Main classes

### Expense

Represents one expense record. It owns the description, amount, date, and identifier. It performs simple validation needed to maintain a valid domain object.

### ExpenseRepository

Defines the repository contract for storing and retrieving expenses. The interface supports adding, getting, updating, removing, listing, and filtering expense records.

### InMemoryExpenseRepository

Implements the repository contract with an in-memory dictionary. It is the only layer that knows how data is stored for this assignment.

### ExpenseService

Coordinates expense operations and applies business rules. It validates input, calls the repository, and raises domain-specific exceptions for invalid or missing data.

### ExpenseCLI

Handles terminal interaction. It reads user input, calls the application service, and formats results. It does not contain domain validation rules or persistence logic.

### ExpenseTrackerApp

Controls the application lifecycle. It creates the repository, service, and CLI, then runs the CLI loop.

## Data model

Each expense contains:

- identifier: unique non-empty string
- description: non-empty string
- amount: positive decimal value
- date: date value in ISO format

## Business rules

1. Each expense must have a unique identifier.
2. Descriptions cannot be empty or whitespace.
3. Amounts must be greater than zero.
4. Dates must be valid date values.
5. Removing or updating an expense requires an existing identifier.
6. Listing and totals must use the current saved records.
7. Filtering must compare case-insensitively against the description or date.

## Validation rules

Validation is performed at the service layer. Invalid input causes a `ValidationError` and prevents data changes.

## Error rules

- `ValidationError`: invalid user or expense data.
- `ExpenseNotFoundError`: requested identifier does not exist.
- `RepositoryError`: storage operation cannot be completed.
- CLI errors are caught and displayed as user-readable messages.
- Unexpected exceptions remain visible to the caller rather than being silently hidden.

## CLI constraints

1. The CLI must use text input and output only.
2. The CLI must not directly modify domain objects.
3. The CLI must not implement business validation.
4. The CLI must return to the main menu after each completed operation.
5. The CLI must exit cleanly when the user selects exit.

## OOP constraints

1. Classes must have one clear responsibility.
2. Service methods must accept and return domain data rather than CLI-specific types.
3. The repository interface must be injectable for future testability.
4. The service must work with any repository implementation that satisfies its contract.
5. Domain entities must not depend on CLI or web implementations.

## Future FastAPI constraints

1. A request layer may call `ExpenseService` directly.
2. Repository interfaces must remain stable when changing the storage implementation.
3. FastAPI request models must be translated to domain values at the API boundary.
4. FastAPI error responses must be mapped from domain exceptions.
5. The CLI and API layers may share the same domain and service behavior.
