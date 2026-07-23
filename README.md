# Car Dealership Inventory System

A full-stack inventory management application for a car dealership. It provides JWT-secured authentication, role-based inventory management, vehicle search, and purchase/restock workflows.

## Technology Stack

- Backend: Python, FastAPI, PyMongo
- Database: MongoDB
- Frontend: React, Vite, Tailwind CSS
- Testing: pytest

## Project Structure

```text
backend/     FastAPI API and backend tests
frontend/    React single-page application
```

## Run locally

1. Copy `backend/.env.example` to `backend/.env` and set `MONGODB_URL`, `MONGODB_DATABASE`, and `JWT_SECRET_KEY`.
2. In `backend`, create a virtual environment, install `requirements.txt`, then run `uvicorn app.main:app --reload`.
3. In `frontend`, run `npm install` once, then `npm run dev`.

The API runs at `http://127.0.0.1:8000` and the Vite application runs at `http://localhost:5173`.

## Features

- JWT registration and sign-in, with user and administrator roles
- Protected vehicle creation, listing, search, editing, purchasing, restocking, and deletion
- Atomic stock reduction that prevents purchasing out-of-stock vehicles
- Customer inventory search and purchase workflow
- Administrator inventory create, edit, restock, and delete workflow

## Verification

Run `python -m pytest -q` in `backend` and `npm.cmd test -- --run` plus `npm.cmd run build` in `frontend`.

## My AI Usage

OpenAI Codex was used to help plan the project structure, reason through requirements, and create initial boilerplate. I will use it as a collaborative development tool while reviewing, testing, and understanding all generated work myself.

The full project-specific AI prompt history is maintained in [PROMPTS.md](PROMPTS.md).
