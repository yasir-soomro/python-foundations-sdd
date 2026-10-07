# Customer Manager Specification

## 1. Problem

A small business needs a simple way to create, review, search, update, and remove customer records from a command-line application. Without a reliable customer list, staff may struggle to find contact information or keep customer records accurate.

## 2. Goal

The goal is to provide a simple Python command-line application that allows users to manage customer information through basic Create, Read, Update, and Delete operations. The application must be easy to use, handle normal input mistakes safely, and allow the user to continue working during one application session.

## 3. Customer Data

Each customer record contains the following information:

- **ID:** A unique identifier that identifies one customer. The application generates this value automatically and the user does not enter it when creating a customer.
- **Name:** The customer's full or display name. The name identifies the customer in lists and searches.
- **Email:** The customer's contact email address. It must be present and must follow a basic email structure.
- **Phone:** The customer's contact phone number. It must be present but does not require advanced phone-number validation.

## 4. Customer ID

- Every customer has a unique ID.
- The application generates the ID automatically.
- The user does not manually assign an ID when creating a customer.
- The ID identifies one customer within the current application session.
- The ID must be used when viewing, updating, or deleting a specific customer.

## 5. Required Operations

### 5.1 Create/Add Customer

The user can create a new customer by providing the customer's name, email, and phone. The application generates a unique ID and stores the customer record.

### 5.2 List Customers

The application displays all stored customers. If no customers exist, it displays an empty-state message instead of an error.

### 5.3 View Customer by ID

The user provides a customer ID. The application displays that customer's complete record. If the ID is invalid or the customer does not exist, the application reports the problem without crashing.

### 5.4 Search Customers

The user can search for customers by name or email. The search must be case-insensitive. The application may display all matching customers when one or more records match.

### 5.5 Update Customer

The user selects an existing customer by ID and provides a new name, email, and phone. The application updates the selected record. The customer's ID must remain unchanged.

### 5.6 Delete Customer

The user provides the ID of an existing customer. The application removes that customer from storage. If the customer does not exist, the operation fails gracefully.

### 5.7 Exit Application

The user can exit the application from the main menu. The application closes cleanly after the exit operation.

## 6. Search Behavior

- Customers may be searched by name.
- Customers may be searched by email.
- Search matching is case-insensitive.
- A search value must be supplied.
- Empty search values are invalid.
- A search that finds no matching customers produces a clear no-results message.

## 7. Update Behavior

An existing customer's information may be updated as follows:

- Name may be changed.
- Email may be changed.
- Phone may be changed.
- The customer ID must remain unchanged.
- Updated values must pass the same validation rules as new customer data.
- The application must not update a customer when the provided data is invalid.

## 8. Delete Behavior

- A customer is deleted using their unique ID.
- The operation requires a valid customer ID.
- If the customer does not exist, the application reports that the customer was not found.
- The application must not crash when deletion fails.

## 9. Validation Rules

The application validates customer data before saving or updating a record.

- Name cannot be empty or contain only whitespace.
- Email cannot be empty or contain only whitespace.
- Email must include a basic structure containing a local part, an @ symbol, and a domain part.
- Phone cannot be empty or contain only whitespace.
- Customer ID must be valid when an ID is required.
- Invalid values must be rejected without changing stored data.

Simple validation is required. The application does not need to perform advanced phone-number or email verification.

## 10. Error Handling

The application must handle normal user mistakes without crashing.

- Invalid menu options must produce a clear message and return to the menu.
- Empty input must be rejected with a clear message.
- Invalid email format must be rejected.
- Invalid customer IDs must be rejected.
- Missing customers must produce a clear not-found message.
- Invalid data must not be saved.
- Errors must return the user to a usable application state.

## 11. Storage

The application uses in-memory storage only.

- No database is used.
- No API is used.
- No external storage is used.
- Customer records remain available only while the current application session is running.
- Data is lost when the application exits unless future functionality adds persistence.

## 12. CLI Behavior

The application provides a simple command-line menu during one user session.

```text
Customer Manager

1. Add Customer
2. List Customers
3. View Customer
4. Search Customers
5. Update Customer
6. Delete Customer
7. Exit
```

The user can choose an operation, complete the required input, view the result, and return to the menu. The user may perform multiple operations in the same session. Invalid menu choices must not terminate the application.

## 13. Architecture Boundary

The following major responsibilities are required at the specification level:

- **Customer data/model:** Represents customer information and its required fields.
- **Customer management/business logic:** Validates customer data and performs create, list, view, search, update, and delete operations.
- **Data storage:** Stores customer records for the current application session.
- **CLI/user interaction:** Reads user input, displays results, and handles menu navigation.

Implementation classes, detailed project structure, frameworks, and libraries belong in the design document, not this specification.

## 14. Non-Goals

This assignment does not include:

- Database persistence
- REST API or other network API
- Web interface
- Authentication
- Authorization
- AI functionality
- External services
- Email or SMS verification
- Advanced search
- Pagination

## 15. Acceptance Criteria

The application is considered successful when the user can:

1. Add a customer and receive a unique customer ID.
2. View all stored customers.
3. View one customer using a valid ID.
4. Search customers by name and email using case-insensitive matching.
5. Update an existing customer's name, email, and phone.
6. Delete an existing customer using their ID.
7. Receive clear errors for invalid input and empty input.
8. Receive clear errors for invalid email values and invalid customer IDs.
9. Receive a clear not-found message when a customer does not exist.
10. Continue using the application after normal input errors.
11. Select an invalid menu option without crashing the application.
12. Exit the application cleanly.
13. Use only in-memory storage for the current application session.

## 16. Specification Completeness

This specification is sufficient to derive requirements, design, implementation, and tests. It defines the business problem, user-facing behavior, customer data, operations, validation, error handling, storage boundary, CLI behavior, non-goals, and measurable acceptance criteria.
