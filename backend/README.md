# Task Management System - Backend

FastAPI-based REST API for task management with authentication, team collaboration, and PostgreSQL database.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis (optional, for caching)

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── task.py
│   │   └── team.py
│   │
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── user.py
│   │   ├── task.py
│   │   └── auth.py
│   │
│   ├── api/                 # API routes
│   │   └── v1/
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── tasks.py     # Task CRUD endpoints
│   │       ├── users.py     # User management
│   │       └── teams.py     # Team collaboration
│   │
│   ├── core/                # Core utilities
│   │   ├── security.py      # Password hashing, JWT
│   │   ├── dependencies.py  # FastAPI dependencies
│   │   └── exceptions.py    # Custom exceptions
│   │
│   └── services/            # Business logic (future)
│
├── tests/                   # Test suite
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── .env.example            # Environment template
```

## 🔑 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login`
3. **Refresh Token**: `POST /api/v1/auth/refresh`

Include the access token in requests:
```
Authorization: Bearer <access_token>
```

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/` - List all users (admin only)

### Tasks
- `GET /api/v1/tasks/` - List tasks with filters
- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

### Teams
- `GET /api/v1/teams/` - List user's teams
- `POST /api/v1/teams/` - Create new team
- `GET /api/v1/teams/{team_id}` - Get team details
- `POST /api/v1/teams/{team_id}/members` - Add team member
- `DELETE /api/v1/teams/{team_id}/members/{user_id}` - Remove member

## 🔧 Development

### Install development dependencies
```bash
pip install -r requirements-dev.txt
```

### Run tests
```bash
pytest
```

### Code formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
mypy app/
```

### Security scan
```bash
bandit -r app/
```

## 🗄️ Database

### Create database
```sql
CREATE DATABASE taskdb;
CREATE USER taskuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
```

### Run migrations (future)
```bash
alembic upgrade head
```

## 🐳 Docker

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

## 📝 Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (generate with `openssl rand -hex 32`)
- `CORS_ORIGINS` - Allowed CORS origins
- `DEBUG` - Enable debug mode

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS protection
- Input validation with Pydantic
- SQL injection prevention (parameterized queries)
- Rate limiting ready
- Security headers

## 📊 Performance

- Connection pooling for database
- Async/await support
- Redis caching ready
- Query optimization with SQLAlchemy

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation
4. Run linters before committing

## 📄 License

MIT License