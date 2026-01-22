# FastAPI Todo Application (Systems-Focused Project)

This repository contains a full-stack Todo application built with **FastAPI**, **SQLAlchemy**, and a server-rendered frontend. The primary purpose of this project was to develop and demonstrate **systems-level understanding** of backend application behavior, rather than frontend design or UI polish.

Most of the HTML, CSS, and JavaScript assets were reused from existing examples so that the majority of effort could be spent on **backend architecture, request handling, authentication, validation, and testing**.

---

## Project Goals

The goal of this project was to move beyond isolated examples and understand how a backend system behaves when:

- Serving real browser traffic
- Handling authenticated API requests
- Validating and persisting user data
- Supporting role-based access (user vs admin)
- Being exercised through automated tests

This repository reflects a learning process focused on **how systems fail, how they are debugged, and how they are stabilized**.

---

## Key Concepts and Learnings

### HTTP Routing and Status Codes
- Practical understanding of:
  - `404 Not Found`
  - `405 Method Not Allowed`
  - `401 Unauthorized` vs `403 Forbidden`
  - `422 Unprocessable Entity`
- Debugged routing issues caused by:
  - Incorrect endpoint paths
  - Trailing slash mismatches
  - Cached frontend JavaScript calling outdated routes

---

### FastAPI Dependency Injection
- Used dependencies to manage:
  - Database session lifecycle
  - Authentication and authorization
- Learned how dependency signatures must align with how request data is delivered
- Centralized authorization checks to avoid duplicated logic across endpoints

---

### Authentication and Authorization
- Implemented JWT-based authentication
- Explored cookie-based vs header-based auth patterns
- Standardized on an API-style `Authorization: Bearer` flow for JavaScript requests
- Implemented role-based access for admin endpoints

This mirrors decisions commonly made in production systems and highlights tradeoffs between security, simplicity, and frontend integration.

---

### Frontend ↔ Backend Integration
While frontend assets were reused, significant effort was spent understanding integration behavior:

- Diagnosed issues where endpoints worked in Swagger but failed in the browser
- Identified browser caching as a source of confusing bugs
- Learned how headers, cookies, and `fetch()` interact with backend dependencies

---

### Validation and Data Modeling
- Used Pydantic models to enforce request schemas
- Learned how required vs optional fields affect POST and PUT behavior
- Interpreted 422 responses as validation signals rather than generic failures
- Adjusted models to better reflect real update semantics

---

### Testing Strategy
- Built automated tests using `pytest` and FastAPI’s test client
- Used dependency overrides to isolate:
  - Database access
  - Authentication behavior
- Tested:
  - Authenticated vs unauthorized access
  - User-specific data isolation
  - Admin-only endpoints
- Balanced response-based assertions with database verification where appropriate

---

## What This Project Emphasizes
- Backend systems thinking
- Real-world debugging across multiple layers
- Authentication and authorization flows
- Validation and correctness
- Test isolation and reliability

## What This Project Does Not Emphasize
- Custom frontend design
- CSS or UI originality
- JavaScript framework usage

Frontend assets were intentionally reused to keep the focus on backend and system behavior.

---

## Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pytest
- Jinja2 Templates
- Vanilla JavaScript (`fetch` API)

---

## Why This Repository Is Public

This project exists to demonstrate:
- Comfort debugging real-world backend issues
- Understanding of how systems behave outside idealized examples
- Ability to reason about tradeoffs and integration points
- Growth through investigation, refactoring, and iteration

It reflects how production development actually works, including mistakes, fixes, and learning along the way.
