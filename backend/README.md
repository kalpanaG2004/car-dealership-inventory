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
