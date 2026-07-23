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

## Deploy (Render + Vercel)

This project is prepared for a free-tier-friendly split deployment: MongoDB Atlas for data, Render for the FastAPI API, and Vercel for the React frontend. This keeps the assignment's React, FastAPI, MongoDB, JWT, and role-based workflows intact.

1. Push the current `main` branch to GitHub. Do not commit `backend/.env`.
2. In Render, select **New > Blueprint** and choose this repository. The included [`render.yaml`](render.yaml) creates the API service. Set these environment variables in the Render service:
   - `MONGODB_URL`: the MongoDB Atlas connection string
   - `MONGODB_DATABASE`: `car_dealership_inventory` (or your chosen database name)
   - `JWT_SECRET_KEY`: a new random secret of at least 32 characters
   - `JWT_ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `60`
3. Deploy Render and confirm `https://<your-api>.onrender.com/api/health` returns `{ "status": "ok" }`.
4. In Vercel, import the same GitHub repository. Set **Root Directory** to `frontend`; Vercel will use `npm run build` and publish `dist` automatically. Add the build-time environment variable `VITE_API_BASE_URL=https://<your-api>.onrender.com` (no trailing slash), then deploy.
5. Copy the production Vercel URL and return to Render. Set `CORS_ORIGINS` to that exact URL, for example `https://car-dealership-inventory.vercel.app`, then redeploy the API. Add a comma-separated preview URL too only if you need browser testing on Vercel previews.
6. Run `python -m scripts.create_admin` from `backend` with the same production environment variables to create the administrator account. Verify customer search/purchase and administrator create, edit, restock, and delete in the deployed site, then capture the four assignment screenshots listed below.

`VITE_API_BASE_URL` is intentionally a frontend build variable; changing it requires a new Vercel deployment. `CORS_ORIGINS` belongs only in Render and must never be `*` because the API accepts bearer credentials.

## Features

- JWT registration and sign-in, with user and administrator roles
- Protected vehicle creation, listing, search, editing, purchasing, restocking, and deletion
- Atomic stock reduction that prevents purchasing out-of-stock vehicles
- Customer inventory search and purchase workflow
- Administrator inventory create, edit, restock, and delete workflow

## Verification

Run `python -m pytest -q` in `backend` and `npm.cmd test -- --run` plus `npm.cmd run build` in `frontend`.

## Submission acceptance checklist

Before recording screenshots, start MongoDB, the FastAPI server, and the Vite app as described above. Create the first administrator with `python -m scripts.create_admin` from `backend`; use a dedicated email and a strong password. Then capture these states in the running application:

1. The sign-in screen and registration link.
2. A customer searching the inventory and purchasing an in-stock vehicle, showing the reduced quantity.
3. An administrator adding a vehicle and editing its details.
4. An administrator restocking and deleting a vehicle.

The automated verification completed on 2026-07-23 consists of 19 backend tests, 5 frontend tests, and a successful frontend production build. A live acceptance run was also completed against MongoDB Atlas on 2026-07-23:

| Workflow | Result |
| --- | --- |
| Customer registration and login | Passed |
| Customer inventory search | Passed (one matching vehicle) |
| Customer purchase | Passed (quantity 2 to 1) |
| Administrator vehicle creation | Passed |
| Administrator restock | Passed (quantity 1 to 4) |
| Administrator edit | Passed (category and price updated) |
| Administrator deletion | Passed (test vehicle removed) |

## Screenshots

Screenshots must be captured with a browser connected to the local Vite application and saved under `docs/screenshots/` using the four states in the acceptance checklist above. Screenshot capture was not possible in the automated delivery environment because no browser was available to control; no placeholder images are included or represented as live evidence.

## My AI Usage

OpenAI Codex was used to help plan the project structure, reason through requirements, and create initial boilerplate. I will use it as a collaborative development tool while reviewing, testing, and understanding all generated work myself.

The full project-specific AI prompt history is maintained in [PROMPTS.md](PROMPTS.md).
