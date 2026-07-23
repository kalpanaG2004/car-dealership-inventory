# AI Tooling Chat History

This log records AI-assisted work performed for this project. It is maintained as work progresses, in line with the assignment requirements.

## 2026-07-23 — Project planning

**User prompt:**

> I have an assignment as part of a company's recruitment process. Below are its details. Go through it then help me navigate through it step by step. I want the backend to be in Python and DB in MongoDB.

**AI assistance:**

The assistant reviewed the requirements, recommended FastAPI, MongoDB, JWT authentication, pytest, React/Vite, and Tailwind CSS, and proposed a test-first implementation and commit sequence.

## 2026-07-23 — Step 1: project foundation

**User prompt:**

> start step 1

**AI assistance:**

The assistant inspected the available tooling and created the initial project layout, dependency manifest, environment examples, Git ignore rules, and this prompt log. No application functionality has been implemented in this step.

## 2026-07-23 — Step 2: backend foundation

**User prompt:**

> start step 2

**AI assistance:**

The assistant guided a test-driven FastAPI foundation: first creating a failing health-check test, then implementing only the application code needed for that test, and finally verifying it with pytest.

## 2026-07-23 — Step 3: authentication

**User prompt:**

> start step 3

**AI assistance:**

The assistant created tests before implementing registration and login. It then added MongoDB configuration, a database dependency, Argon2 password hashing, duplicate-email protection, and JWT login tokens. The tests use a mock MongoDB instance only for isolation; the application configuration targets a real MongoDB connection.

## 2026-07-23 — Step 4: protected vehicle creation

**User prompt:**

> start step 4

**AI assistance:**

The assistant created tests before implementing the protected vehicle-creation endpoint. It then added bearer-token validation, current-user lookup from MongoDB, vehicle request validation, and persisted vehicle creation.

## 2026-07-23 — Step 5: vehicle listing and search

**User prompt:**

> start step 5

**AI assistance:**

The assistant created tests before implementing protected vehicle listing and search. It added case-insensitive make, model, and category filters, plus inclusive minimum and maximum price filters.

## 2026-07-23 — Step 6: vehicle update and administration

**User prompt:**

> continue step 6

**AI assistance:**

The assistant continued from the existing Red-phase tests, implemented partial vehicle updates for authenticated users, and restricted deletion to administrators. It also added a local password-hidden script for creating the first administrator account through the configured MongoDB connection.

## 2026-07-23 — Step 7: purchasing and restocking

**User prompt:**

> start step 7

**AI assistance:**

The assistant created tests before implementing purchase and restock workflows. It used a conditional MongoDB update to prevent stock from going below zero, returned a clear out-of-stock response, and restricted restocking to administrators.
