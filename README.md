# FastAPI Task Management API - Learning Project

A comprehensive Task Management API built with FastAPI to learn modern web API development, authentication, and database operations.

## Learning Objectives

This project was created to understand and implement:
- **FastAPI Framework**: Modern Python web framework for building APIs
- **OAuth2 Authentication**: JWT token-based authentication system
- **Database Operations**: SQLAlchemy ORM with SQLite database
- **API Design**: RESTful API principles and best practices
- **Data Validation**: Pydantic models for request/response validation
- **Database Relationships**: User-Task relationship modeling

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SQLite**: Lightweight database for data storage
- **Pydantic**: Data validation using Python type annotations
- **JWT (JSON Web Tokens)**: For secure authentication
- **Passlib**: Password hashing library
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
Delta/
├── main.py          # FastAPI application and API endpoints
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic schemas for data validation
├── crud.py          # Database operations (Create, Read, Update, Delete)
├── database.py      # Database configuration and connection
└── README.md        # Project documentation
```

## Architecture Overview

### Database Layer (`models.py`)
- **UserDb**: User table with authentication fields
- **TaskDb**: Task table with foreign key relationship to users
- **Relationships**: One-to-many relationship (User → Tasks)

### Schema Layer (`schemas.py`)
- **User Schemas**: UserCreate, User, UserInDB for different contexts
- **Task Schemas**: TaskBase, Task for request/response validation
- **Auth Schemas**: TokenData for JWT token handling

### Business Logic (`crud.py`)
- **Authentication**: User creation, password hashing, token generation
- **Task Operations**: CRUD operations for tasks with user isolation
- **Security**: Password verification, token validation

### API Layer (`main.py`)
- **Authentication Endpoints**: User registration, login
- **Task Endpoints**: Full CRUD operations for tasks
- **Security**: Protected endpoints with JWT authentication

## Authentication Flow

1. **User Registration**: Create account with username/password
2. **Login**: Exchange credentials for JWT access token
3. **Token Usage**: Include token in Authorization header for protected endpoints
4. **Token Validation**: Automatic verification on each request

```python
# Example token usage
headers = {"Authorization": "Bearer <your_jwt_token>"}
```

## Database Schema

### Users Table
- `id`: Primary key (auto-increment)
- `username`: Unique username
- `full_name`: User's full name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status

### Tasks Table
- `id`: Primary key (auto-increment)
- `name`: Task name
- `description`: Task description
- `deadline`: Task deadline (date)
- `reminder`: Reminder datetime
- `status`: Enum ('Pending', 'Completed')
- `priority`: Enum ('High', 'Medium', 'Low')
- `user_id`: Foreign key to users table

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /create-user` - Register new user

### Task Management
- `POST /add-task/` - Create new task
- `GET /tasks/` - Get all user tasks (with pagination)
- `GET /tasks/{id}/` - Get specific task by ID
- `PUT /update-task/{id}/` - Update existing task
- `DELETE /delete-task/{id}/` - Delete task

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone/Download the project files**
   ```bash
   git clone Task-API
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy passlib python-jose bcrypt python-multipart
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - API: http://127.0.0.1:8000
   - Interactive Documentation: http://127.0.0.1:8000/docs
   - Alternative Documentation: http://127.0.0.1:8000/redoc


## Key Learning Outcomes

### FastAPI Features Learned
- **Automatic API Documentation**: Swagger UI and ReDoc generation
- **Type Hints**: Python type annotations for better code quality
- **Dependency Injection**: Using `Depends()` for database sessions and authentication
- **Request/Response Models**: Pydantic schemas for data validation
- **Error Handling**: HTTP exception handling with proper status codes

### Authentication Concepts
- **JWT Tokens**: Stateless authentication mechanism
- **Password Hashing**: Secure password storage with bcrypt
- **OAuth2**: Industry-standard authorization framework
- **Token Expiration**: Time-based token validity

### Database Operations
- **ORM Usage**: SQLAlchemy for database abstraction
- **Relationships**: Foreign keys and table relationships
- **Query Optimization**: Efficient database queries with filters
- **Transaction Management**: Database commits and rollbacks

### Security Best Practices
- **Password Security**: Never store plain text passwords
- **User Isolation**: Each user can only access their own tasks
- **Token Validation**: Verify authentication on protected endpoints
- **Input Validation**: Validate all incoming data
