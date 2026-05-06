# Todo App - FastAPI + PostgreSQL

A full-stack Todo Management Application built using **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, and **Jinja2 Templates** with secure JWT-based authentication and role-based access control.

## Live Demo

🔗 [https://todo-app-joax.onrender.com/auth/login-page]

---

# Features

* User Registration & Login
* JWT Authentication
* Password Hashing using bcrypt
* Role-Based Authorization (User/Admin)
* Create, Update, Delete Todos
* PostgreSQL Database Integration
* SQLAlchemy ORM
* Alembic Database Migrations
* Jinja2 Frontend Templates
* Bootstrap UI
* Environment Variable Configuration
* Render Deployment
* Neon PostgreSQL Integration

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT Authentication
* Passlib (bcrypt)

## Frontend

* HTML
* CSS
* Bootstrap
* Jinja2 Templates

## Deployment

* Render
* Neon PostgreSQL

---

# Project Structure

```bash
TODOAPP/
│
├── alembic/
├── routers/
├── static/
├── templates/
├── models.py
├── database.py
├── config.py
├── main.py
├── requirements.txt
└── alembic.ini
```

---

# Authentication Flow

* Users register with secure password hashing
* JWT access token generated after login
* Protected routes require authentication
* Admin routes protected using role-based authorization

---

# Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
SQLALCHEMY_DATABASE_URL=your_database_url
```

---

# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/dhruv4326/Todo-List.git
cd Todo-List
```

## Create Virtual Environment

```bash
python -m venv fastapienv
```

## Activate Environment

### Windows

```bash
fastapienv\Scripts\activate
```

### Linux/Mac

```bash
source fastapienv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Alembic Migrations

```bash
alembic upgrade head
```

---

# Run Application

```bash
uvicorn main:app --reload
```

Application will run on:

```text
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Security Improvements

* Environment variables used for sensitive credentials
* Public admin role assignment removed
* JWT-based authentication
* Password hashing using bcrypt

---

# Future Improvements

* Docker Deployment
* CI/CD Pipeline
* Email Verification
* Password Reset
* Better Admin Dashboard
* Responsive UI Enhancements

---

# Author

Dhruv

GitHub: https://github.com/dhruv4326
