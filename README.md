# FastAPI Todo Application

A full-stack todo application built with FastAPI, PostgreSQL, SQLAlchemy, and a server-rendered frontend. The project focuses on backend architecture, authentication, authorization, validation, database persistence, testing, and browser-to-API integration.

## Live Demo

**[Open the deployed application](https://fastapi-todo-app-80kh.onrender.com/)**

Interactive API documentation is available at:

- [Swagger UI](https://fastapi-todo-app-80kh.onrender.com/docs)
- [ReDoc](https://fastapi-todo-app-80kh.onrender.com/redoc)

The app is hosted on Render, so the first request may take a moment if the service has been inactive.

## Project Overview

Users can create an account, sign in, and manage a private todo list. Each todo belongs to its creator, and authenticated users can only retrieve or modify their own records. Administrative endpoints provide role-protected access to all users and todos.

The frontend uses Jinja2 templates and vanilla JavaScript so the project can demonstrate a complete browser workflow without hiding the backend behavior behind a frontend framework.

## Features

- User registration with bcrypt password hashing
- OAuth2 password flow and JWT access tokens
- Cookie-based browser session integration
- User-specific todo data isolation
- Create, view, update, complete, and delete todos
- Priority validation from 1 through 5
- User profile, password, and phone-number endpoints
- Role-based authorization for administrative routes
- PostgreSQL persistence through SQLAlchemy
- Server-rendered pages with Jinja2
- Static JavaScript and CSS assets
- Automatic Swagger UI and ReDoc documentation
- Health-check endpoint
- Automated API tests with pytest
- Database and authentication dependency overrides for isolated tests

## Tech Stack

| Area | Technology |
|---|---|
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | OAuth2, JWT, python-jose, Passlib, bcrypt |
| Frontend | Jinja2, HTML, CSS, vanilla JavaScript |
| Testing | pytest, FastAPI TestClient, HTTPX |
| Server | Uvicorn |
| Deployment | Render |

## Application Flow

1. A visitor registers through the browser form.
2. Passwords are hashed before the user record is stored.
3. The user signs in through the OAuth2 token endpoint.
4. The returned JWT is stored in a browser cookie.
5. JavaScript sends the token in the `Authorization: Bearer` header for protected API requests.
6. FastAPI dependencies validate the token and provide the authenticated user to each route.
7. Todo queries are filtered by `owner_id` so users only access their own records.

## API Routes

### General

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/` | Redirect to the todo page |
| `GET` | `/healthy` | Application health check |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

### Authentication

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/auth/login-page` | Render the login page |
| `GET` | `/auth/register-page` | Render the registration page |
| `POST` | `/auth/` | Register a user |
| `POST` | `/auth/token` | Authenticate and issue a JWT |

### Todos

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/todos/todo-page` | Render the authenticated user's todos |
| `GET` | `/todos/add-todo-page` | Render the add-todo form |
| `GET` | `/todos/edit-todo-page/{todo_id}` | Render the edit form |
| `GET` | `/todos/` | Return the authenticated user's todos |
| `GET` | `/todos/{todo_id}` | Return one owned todo |
| `POST` | `/todos/` | Create a todo |
| `PUT` | `/todos/{todo_id}` | Update an owned todo |
| `DELETE` | `/todos/{todo_id}` | Delete an owned todo |

### User Account

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/user/` | Return the authenticated user's profile |
| `PUT` | `/user/` | Change the authenticated user's password |
| `PUT` | `/user/{phone_number}` | Update the authenticated user's phone number |

### Administration

These routes require a JWT containing the `admin` role.

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/admin/todo` | Return all todos |
| `GET` | `/admin/users` | Return all users |
| `DELETE` | `/admin/todo/{todo_id}` | Delete any todo |
| `DELETE` | `/admin/user/{user_id}` | Delete any user |

## Validation and Authorization

Todo request bodies are validated with Pydantic:

```json
{
  "title": "Finish FastAPI project",
  "description": "Complete documentation and testing",
  "priority": 3,
  "complete": false
}
```

The application enforces:

- A minimum title length of 3 characters
- A description length between 3 and 100 characters
- A priority greater than 0 and less than 6
- Authentication for protected routes
- Ownership checks for individual todo operations
- Administrative role checks for `/admin` routes

## Project Structure

```text
fastapi-todo-app/
├── app/
│   ├── main.py              # Application setup and router registration
│   ├── database.py          # Engine, session factory, and DB dependency
│   ├── models.py            # SQLAlchemy user and todo models
│   └── routers/
│       ├── auth.py          # Registration, login, JWT creation and validation
│       ├── todos.py         # Todo pages and CRUD endpoints
│       ├── users.py         # User profile and account updates
│       └── admin.py         # Administrator-only endpoints
├── static/                  # Browser JavaScript and styles
├── templates/               # Jinja2 page templates
├── tests/
│   ├── conftest.py          # Database fixtures and dependency overrides
│   ├── test_auth.py         # Authentication tests
│   ├── test_todos.py        # Todo CRUD and ownership tests
│   └── test_admin.py        # Administrative authorization tests
├── requirements.txt
└── README.md
```

## Run Locally

### Prerequisites

- Python 3.11 or newer
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/timmuh03/fastapi-todo-app.git
cd fastapi-todo-app
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/TodoApplicationDatabase
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit real credentials or secret keys.

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

## Run the Tests

The test suite uses a separate PostgreSQL database and wraps each test in a transaction so changes can be rolled back.

1. Create a local test database.
2. Update the test database connection in `tests/conftest.py` for your environment.
3. Run:

```bash
pytest
```

The tests cover authentication, JWT claims, todo CRUD operations, record ownership, admin permissions, unauthorized requests, missing resources, and database state changes.

## Systems-Focused Learning

This project was built to develop practical understanding of how a backend application behaves when it:

- Serves browser traffic and API requests
- Coordinates templates, JavaScript, and protected endpoints
- Validates and persists user-controlled data
- Distinguishes authentication failures from authorization failures
- Prevents users from accessing one another's records
- Handles status codes such as `401`, `403`, `404`, `405`, and `422`
- Uses dependency injection for database and authentication concerns
- Is tested with controlled identities and isolated database sessions

Most frontend styling and assets were adapted from existing examples so development time could remain focused on backend behavior, integration, debugging, and test reliability.

## Author

Created by [Tim Muhlestein](https://github.com/timmuh03).
