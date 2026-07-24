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

## 2026-07-23 — Step 8: complete frontend workflows

**User prompt:**

> study the current folder structure and complete the assignment as instructed originally. complete it step by step. complete the whole step in one go, all phases altogether, commit, then give me the prompt for next step

**AI assistance:**

The assistant completed the React application workflows against the existing FastAPI API: registration and login, inventory loading and search, purchasing, and administrator vehicle creation, editing, restocking, and deletion. It added a UI purchase test, verified the frontend test/build and backend regression suites, and updated the run documentation.

## 2026-07-23 — Step 9: delivery validation

**User prompt:**

> Start the final delivery step: run the full application locally with MongoDB, create an administrator account, perform a manual end-to-end acceptance test for customer and admin workflows, capture screenshots, and finalize the README submission documentation.

**AI assistance:**

The assistant started the local FastAPI and Vite services and verified the health endpoint. The configured MongoDB Atlas connection did not respond during administrator creation, and no controllable browser was available for screenshots in this environment. It finalized the README with reproducible startup instructions and a live acceptance/screenshot checklist; the live database and screenshot portions must be rerun once MongoDB connectivity and a browser are available.

## 2026-07-23 — Step 10: live acceptance validation

**User prompt:**

> MongoDB Atlas access is enabled. Run the live customer and admin acceptance test, capture and save the required screenshots, update the README with their paths, and commit the final delivery assets.

**AI assistance:**

The assistant confirmed Atlas connectivity, created a delivery administrator, and performed a live API acceptance test: customer registration/login/search/purchase and administrator vehicle creation/restock/edit/deletion all passed. The temporary test vehicle was deleted after the run. The browser runtime still had no available browser, so screenshots could not be captured or falsely represented; the README records the verified results and required screenshot directory.

## 2026-07-24 — Step 11: production deployment and delivery finalization

**User prompt:**

> i have now successfully deployed my backend on render https://car-dealership-inventory-t8ip.onrender.com & frontend on vercel https://car-dealership-inventory-eey6rqeaa-kalpanag2004s-projects.vercel.app/
> now what are the changes that i need to do in my documentations to showcase these. let's finalize the project now with an apt commit aligned with the assignment

**AI assistance:**

The assistant updated the README to record the live Vercel frontend, Render API, Swagger documentation, and health-check URLs. It also clarified that screenshots must be taken from the deployed application and saved as submission evidence, without claiming screenshots that were not captured. The deployment documentation and this AI usage history were finalized in a documentation-only commit.
