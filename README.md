# Python Foundations SDD

A Python learning repository organized around Spec-Driven Development (SDD). Each assignment progresses from a business specification through requirements, design, implementation, testing, and verification.

## Assignments

1. Expense Tracker
2. Customer Manager
3. Ticket Manager
4. Validation System
5. Exception Handling
6. Async API Caller

## Project Setup

This project uses Python 3.12 or newer and the `uv` package manager.

```powershell
uv sync
uv run --python 3.14 python -m unittest discover -s assignments/01-expense-tracker/tests -v
```

Use a compatible installed Python version when Python 3.12+ is not available.

## Development Approach

Each assignment follows this order:

1. Understand the specification.
2. Define requirements.
3. Create the design.
4. Implement only the approved behavior.
5. Add focused tests.
6. Run the relevant tests.
7. Report the actual results.

## Testing

The repository uses Python's built-in `unittest` framework. Run tests from the repository root with:

```powershell
uv run --python 3.14 python -m unittest discover -s assignments/01-expense-tracker/tests -v
```

Replace the assignment path with the desired assignment when running a different test suite.

## Repository Structure

```text
.
├── assignments/
│   ├── 01-expense-tracker/
│   ├── 02-customer-manager/
│   ├── 03-ticket-manager/
│   ├── 04-validation-system/
│   ├── 05-exception-handling/
│   └── 06-async-api-caller/
├── docs/
├── pyproject.toml
├── README.md
├── STANDING_RULES.md
└── uv.lock
```
