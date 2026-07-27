# Task API

A RESTful task management API built with **Python (FastAPI)**, featuring JWT authentication, per-user data isolation, and a persistent SQLite database — containerized with **Docker** and tested with **pytest**.

## Features

- User signup and login with JWT-based authentication
- Passwords securely hashed with bcrypt (never stored in plain text)
- Full CRUD for tasks (create, read, update, delete)
- Each user can only access their own tasks
- Persistent storage via SQLite + SQLAlchemy ORM
- Dockerized for consistent, portable deployment
- Automated test suite (pytest) covering auth, ownership, and CRUD operations
- Continuous Integration via GitHub Actions

## Tech Stack

Python · FastAPI · SQLAlchemy · SQLite · JWT (python-jose) · bcrypt (passlib) · Docker · pytest · GitHub Actions · Git

## Project layout

task-api/
├── app/
│ ├── main.py # API routes
│ ├── models.py # Database table definitions
│ ├── database.py # Database connection setup
│ └── auth.py # Password hashing & JWT tokens
├── tests/
│ └── test_main.py # Automated test suite
├── .github/workflows/
│ └── ci.yml # CI pipeline
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md


## Running locally

```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows
# source .venv/bin/activate        # Mac/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Running with Docker

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

## Running tests

```bash
python -m pytest -v
```

## API Overview

| Method | Endpoint | Description | Auth required |
|--------|----------|--------------|----------------|
| POST | `/signup` | Create a new account | No |
| POST | `/login` | Log in, receive a JWT token | No |
| GET | `/tasks` | List your tasks | Yes |
| POST | `/tasks` | Create a task | Yes |
| GET | `/tasks/{id}` | Get a single task | Yes |
| PUT | `/tasks/{id}` | Update a task | Yes |
| DELETE | `/tasks/{id}` | Delete a task | Yes |

## Notes

Migrated from in-memory storage to a persistent SQLite database, and resolved a real dependency conflict between `passlib` and `bcrypt` during authentication setup.
