# Backend

The FastAPI backend will be implemented test-first in the following stages:

1. Application configuration and health check
2. Authentication and role-based access control
3. Vehicle inventory CRUD operations
4. Search, purchasing, and restocking

Copy `.env.example` to `.env` and configure a MongoDB connection before running the application.

## Local development

From the `backend` directory on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

The health endpoint is available at `GET /api/health`.

## Authentication

Configure `MONGODB_URL`, `MONGODB_DATABASE`, and a strong `JWT_SECRET_KEY` in `backend/.env` before using the authentication endpoints against a real database. The API provides:

- `POST /api/auth/register`
- `POST /api/auth/login`

Public registration always creates a `user` account. Administrative roles will be created through a controlled setup flow in a later step.

## Inventory progress

The following routes require a valid Bearer token:

- `POST /api/vehicles`
- `GET /api/vehicles`
- `GET /api/vehicles/search?make=&model=&category=&min_price=&max_price=`

Search text filters are case-insensitive and partial matches. The remaining update, deletion, purchase, and restock endpoints will be added in subsequent test-driven steps.
