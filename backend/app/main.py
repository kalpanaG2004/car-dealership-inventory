from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicles_router

app = FastAPI(
    title="Car Dealership Inventory API",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(vehicles_router)


@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a lightweight status response without requiring a database call."""
    return {"status": "ok"}
