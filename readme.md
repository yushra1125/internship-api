# Internship API

A REST API built using Python, FastAPI, SQLAlchemy, and PostgreSQL. This project manages users and their assigned tasks with database integration and input validation.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- Git and GitHub
- Postman

## Features

### User Management
- Create a user
- Get all users
- Get user by ID
- Update user details
- Delete a user
- View user details with assigned tasks

### Task Management
- Create a task and assign it to a user
- Get all tasks
- Get task by ID
- Update a task
- Delete a task
- Filter tasks by status

### Validation and Error Handling
- Pydantic request validation
- Custom 404 error responses
- Custom 422 validation error responses
- Check whether an assigned user exists

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
4. Add your database connection string:

   ```env
   DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/internship_db
   ```

   Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Run the API

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create user |
| GET | `/users` | Get all users |
| GET | `/users/{user_id}` | Get user by ID |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

Filter tasks by status:

`GET /tasks?task_status=pending`

Available statuses: `pending`, `in_progress`, `completed`.

## Health Check

`GET /health`

Returns the API health status.

## Git Branch

`feature/api-setup`

## Author

Internship Project – AS Infosolution