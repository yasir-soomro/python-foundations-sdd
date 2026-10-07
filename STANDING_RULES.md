# Standing Rules

## Development approach

- Use Spec-Driven Development (SDD).
- Complete one assignment at a time.
- Complete one step at a time.
- Never move to the next step without explicit approval.
- Create the design and plan before writing code.
- Use modern Python 3.12 or newer.
- Use object-oriented programming with clear responsibilities.
- Use type hints, clean architecture, and small modules.
- Keep business logic separate from CLI code.
- Keep core logic reusable for a future FastAPI conversion.
- Do not invent requirements or features.
- Use asynchronous I/O only where real I/O requires it.

## Architecture

The repository should follow this dependency direction:

```text
CLI / Future FastAPI
        ↓
Application Services
        ↓
Domain
        ↓
Infrastructure
```

## Testing and quality

- Write tests for important behavior.
- Handle errors properly and never hide exceptions.
- Do not claim that tests pass unless they have been run.
- Validate behavior with focused tests before reporting completion.

## Assignment workflow

1. Review the assignment specification.
2. Produce the design and plan.
3. Wait for approval before implementation.
4. Implement only the approved step.
5. Add or update tests for important behavior.
6. Run the relevant test command.
7. Report the actual results.
8. Stop after the step and wait for approval before continuing.

## Repository assignments

1. Expense Tracker
2. Customer Manager
3. Ticket Manager
4. Validation System
5. Exception Handling
6. Async API Caller
