# Internship API

A REST API built using Python 3.13, FastAPI, SQLAlchemy, and PostgreSQL. It provides secure JWT authentication, session management, role-based access control (RBAC), and task management for teachers and students.

## Technologies Used

- Python 3.13
- FastAPI and Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- JWT Authentication
- Password Hashing
- Pytest
- Git and GitHub
- Swagger UI

## Features

### Authentication

- Student registration and login
- Secure password hashing (passwords are never stored as plain text)
- JWT access and refresh tokens
- Access-token expiry and refresh functionality
- Session tracking and refresh-token hashing
- Logout with session revocation
- Authenticated user profile endpoint
- Rejection of expired and revoked sessions

### Role-Based Access Control

**Teacher**
- Create and assign tasks to students
- View all tasks and users
- View individual tasks and user details
- Update and delete tasks

**Student**
- View only their assigned tasks
- Update their own task status
- Add work notes
- View their own profile
- Update their own profile (name, email, and phone)
- Cannot create, assign, or delete tasks
- Cannot access another student's tasks or teacher-only data

### Task Management

Available task statuses:

- `pending`
- `in_progress`
- `done`

### Validation and Error Handling

- Pydantic request validation
- Invalid login rejection
- Authentication and authorization checks
- 401 Unauthorized responses
- 403 Forbidden responses
- 404 Not Found responses
- 422 Validation error responses

## Project Setup

Clone the repository:

```bash
git clone https://github.com/yushra1125/internship-api.git
cd internship-api
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Configuration

1. Install PostgreSQL.
2. Create a database named `internship_db`.
3. Create a `.env` file in the project root.
4. Add the following variables:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/internship_db
SECRET_KEY=YOUR_SECRET_KEY
```

Replace the database password with your own PostgreSQL password.

Generate a secure secret key locally:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value into `SECRET_KEY` in your local `.env` file.

**Important:** Never commit `.env`, database passwords, secret keys, or access tokens to GitHub.

## Database Migrations

Check the current migration version:

```bash
alembic current
```

Apply migrations:

```bash
alembic upgrade head
```

Generate a migration after changing database models:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Revert the last migration if required:

```bash
alembic downgrade -1
```

## Create a Teacher Account

Run the seed script:

```bash
python seed.py
```

Follow the prompts to create the teacher account. Use your own credentials locally.

Students can register through:

`POST /auth/register`

## Run the API

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Swagger UI:

http://127.0.0.1:8000/docs

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a student |
| POST | `/auth/login` | Login and receive tokens |
| POST | `/auth/refresh` | Refresh tokens |
| POST | `/auth/logout` | Revoke session |
| GET | `/auth/me` | Get current user profile |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create a user (teacher) |
| GET | `/users` | Get all users (teacher) |
| GET | `/users/{user_id}` | Get user by ID (teacher) |
| PUT | `/users/{user_id}` | Update a user (teacher) |
| DELETE | `/users/{user_id}` | Delete a user (teacher) |
| PATCH | `/users/me` | Update own profile (student) |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create and assign a task (teacher) |
| GET | `/tasks` | Get all tasks (teacher) |
| GET | `/tasks/my` | Get own assigned tasks (student) |
| GET | `/tasks/{task_id}` | Get task by ID (teacher) |
| PUT | `/tasks/{task_id}` | Update a task (teacher) |
| PATCH | `/tasks/{task_id}/work` | Update own task status and work note (student) |
| DELETE | `/tasks/{task_id}` | Delete a task (teacher) |

## Authentication Flow

1. Register a student or create a teacher account using the seed script.
2. Login using email and password.
3. Receive an access token and refresh token.
4. Use the access token as a Bearer token for protected endpoints.
5. Use the refresh endpoint when a new token pair is needed.
6. Logout to revoke the session.

Protected endpoints require a valid access token and an active session.

## Testing

Run automated tests:

```bash
python -m pytest -q
```

The test suite currently contains **25 passing tests** covering:

- User creation and input validation
- Successful and unsuccessful login
- Authenticated profile access
- Missing authentication token
- Logout and session revocation
- Refresh-token rejection after logout
- Expired access-token and refresh-token rejection
- Student access to their own tasks
- Student task-status and work-note updates
- Student restrictions on task creation and deletion
- Prevention of access to another student's tasks
- Prevention of updating another student's task
- Student profile updates and duplicate-email validation
- Teacher access restrictions on student profile updates
- Teacher task updates and deletion
- Rejection of task assignment to an invalid student

API endpoints can also be tested manually using Swagger UI or Postman.

## Git Branch

`feature/api-setup`

## Author

Internship API Project
