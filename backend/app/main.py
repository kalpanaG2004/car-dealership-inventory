from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicles_router

app = FastAPI(
    title="Car Dealership Inventory API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vehicles_router)


@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a lightweight status response without requiring a database call."""
    return {"status": "ok"}
