# Doorstop MCP Workflow Example

This example demonstrates a complete workflow using the Doorstop MCP tools to manage requirements for a sample project.

## Scenario: Developing a User Authentication System

### Step 1: Check Current State

```python
# First, let's see what documents we have
list_documents()

# Check existing requirements
list_items(prefix="REQ")

# Check existing tests
list_items(prefix="TST")
```

### Step 2: Create New Requirements

```python
# Create a high-level authentication requirement
create_item(
    prefix="REQ",
    text="The system shall implement secure user authentication",
    req_type="Functional",
    verification_method="Test",
    header="Secure Authentication"
)

# Create a password policy requirement
create_item(
    prefix="REQ",
    text="The system shall enforce password complexity rules with minimum 12 characters including uppercase, lowercase, numbers, and special characters",
    req_type="Non-Functional",
    verification_method="Inspection",
    header="Password Complexity"
)

# Create a session management requirement
create_item(
    prefix="REQ",
    text="The system shall implement session timeout after 30 minutes of inactivity",
    req_type="Functional",
    verification_method="Demonstration",
    header="Session Timeout"
)
```

### Step 3: Create Corresponding Tests

```python
# Test for authentication functionality
create_item(
    prefix="TST",
    text="Verify that users can authenticate with valid credentials and are rejected with invalid credentials",
    req_type="Functional",
    verification_method="Test",
    header="Authentication Validation"
)

# Test for password policy
create_item(
    prefix="TST",
    text="Verify that passwords not meeting complexity requirements are rejected during account creation",
    req_type="Non-Functional",
    verification_method="Test",
    header="Password Policy Enforcement"
)

# Test for session timeout
create_item(
    prefix="TST",
    text="Verify that user sessions are automatically terminated after 30 minutes of inactivity",
    req_type="Functional",
    verification_method="Demonstration",
    header="Session Timeout Verification"
)
```

### Step 4: Create Low-Level Requirements

```python
# Technical implementation details
create_item(
    prefix="LLR",
    text="The authentication system shall use JWT tokens with HS256 algorithm for session management",
    req_type="Technical",
    verification_method="Code Review",
    header="JWT Implementation"
)

create_item(
    prefix="LLR",
    text="Password hashing shall use bcrypt with a minimum cost factor of 12",
    req_type="Technical",
    verification_method="Code Review",
    header="Password Hashing"
)

create_item(
    prefix="LLR",
    text="Session timeout shall be implemented using server-side session tracking with Redis",
    req_type="Technical",
    verification_method="Code Review",
    header="Session Tracking"
)
```

### Step 5: Verify the Complete Structure

```python
# Check the updated document hierarchy
list_documents()

# Review all requirements
list_items(prefix="REQ")

# Review all tests
list_items(prefix="TST")

# Review all low-level requirements
list_items(prefix="LLR")
```

### Step 6: Find Specific Document Details

```python
# Get details about the REQ document
find_document(prefix="REQ")

# Get details about the TST document
find_document(prefix="TST")
```

## Best Practices Demonstrated

1. **Traceability**: Each high-level requirement (REQ) has corresponding tests (TST) and technical implementations (LLR)
2. **Consistent Formatting**: All requirements use "The system shall..." format
3. **Proper Classification**: Requirements are clearly marked as Functional, Non-Functional, or Technical
4. **Verification Methods**: Appropriate verification methods are specified for each requirement
5. **Atomic Requirements**: Each requirement addresses a single, specific aspect of the system

## Expected Output Structure

After running this workflow, you should have:

- **3 new REQ items** (authentication, password policy, session timeout)
- **3 new TST items** (corresponding tests for each requirement)
- **3 new LLR items** (technical implementation details)

The document hierarchy will show:
```
REQ
│   
├── TST (3 test cases)
│   
└── LLR (3 technical implementations)
```

This workflow ensures complete traceability from high-level requirements through to implementation and testing.