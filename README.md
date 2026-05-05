# Todo List API

A backend Todo REST API built with FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, and role-based access control.

## Features

- User registration and login
- JWT-based authentication
- Password hashing using bcrypt
- Create, read, update, and delete todos
- User-specific todo access
- Admin-only routes to view and delete all todos
- Update user password
- Update user phone number
- PostgreSQL database integration
- Environment-based secret management using `.env`

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT / python-jose
- Passlib bcrypt
- Alembic

## Project Structure

```bash
Todo-List/
│
├── alembic/
├── routers/
│   ├── auth.py
│   ├── todos.py
│   ├── admin.py
│   └── Users.py
│
├── database.py
├── models.py
├── main.py
├── alembic.ini
├── .gitignore
└── README.md

