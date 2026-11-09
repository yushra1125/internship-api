# Internship API

A REST API built using Python, FastAPI, SQLAlchemy, and PostgreSQL. This project provides secure user authentication, JWT-based authorization, role-based access control (RBAC), and task management.

## Technologies Used

- Python 3.13
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- JWT Authentication
- Password Hashing
- Git and GitHub
- Swagger UI

## Features

### Authentication
- User registration and login
- Secure password hashing
- JWT access and refresh tokens
- Token refresh functionality
- Logout with session revocation
- Get currently authenticated user profile
- Session expiry and revoked-token validation

### Role-Based Access Control

**Teacher**
- Create and assign tasks to students
- View all tasks
- Update and delete tasks
- View users and their information

**Student**
- View only assigned tasks
- Update their own task status
- Add and update work notes
- View their own profile
- Cannot create, assign, or delete tasks
- Cannot access other students' tasks

### Task Management
- Create and assign tasks
- Get all tasks (teacher only)
- Get tasks assigned to the logged-in student
- Get task by ID (teacher only)
- Update and delete tasks (teacher only)
- Update task status and work notes (student only)

Available task statuses:
- `pending`
- `in_progress`
- `completed`

### Validation and Error Handling
- Pydantic request validation
- Password verification
- Authentication and authorization checks
- Custom 404 error responses
- 401 Unauthorized responses
- 403 Forbidden responses
- 422 Validation error responses

## Project Setup

1. Clone the repository:

```bash
git clone https://github.com/yushra1125/internship-api.git
```

2. Open the project folder:

```bash
cd internship-api
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Configuration

1. Install PostgreSQL.
2. Create a database named `internship_db`.
3. Create a `.env` file in the project root directory.
4. Add the following environment variables:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/internship_db
SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholders with your own PostgreSQL password and a secure secret key.

**Important:** Never commit your `.env` file or real passwords to GitHub.

## Alembic Migrations

Alembic is used to manage database schema changes.

Check the current migration version:

```bash
alembic current
```

Generate a migration after changing database models:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Revert the last migration:

```bash
alembic downgrade -1
```

## Run the API

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI:

http://127.0.0.1:8000/docs

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a student |
| POST | `/auth/login` | Login and receive tokens |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Revoke session |
| GET | `/auth/me` | Get current user profile |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create user (as permitted by role) |
| GET | `/users` | Get all users (teacher only) |
| GET | `/users/{user_id}` | Get user by ID |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create and assign task (teacher) |
| GET | `/tasks` | Get all tasks (teacher) |
| GET | `/tasks/my` | Get own assigned tasks (student) |
| GET | `/tasks/{task_id}` | Get task by ID (teacher) |
| PUT | `/tasks/{task_id}` | Update task (teacher) |
| PATCH | `/tasks/{task_id}/work` | Update own task status and work note (student) |
| DELETE | `/tasks/{task_id}` | Delete task (teacher) |

## Authentication Flow

1. Register a student or use an existing teacher account.
2. Login using email and password.
3. Receive an access token and refresh token.
4. Authorize requests using the access token.
5. Use the refresh endpoint to obtain new tokens.
6. Logout to revoke the current session.

Protected endpoints require a valid access token.

## Testing

API endpoints can be tested using Swagger UI or Postman.

The following scenarios were tested:

- Teacher login and authentication
- Student login and authentication
- Teacher creates and assigns tasks
- Student views assigned tasks
- Student updates task status and work notes
- Student cannot create or delete tasks
- Student cannot access another student's task
- Student cannot access the teacher-only users list
- Invalid login credentials
- Missing authentication token
- User profile access

## Git Branch

`feature/api-setup`

## Author

Internship API Project