from fastapi import FastAPI

app = FastAPI(
    title="Car Dealership Inventory API",
    version="0.1.0",
)


@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a lightweight status response without requiring a database call."""
    return {"status": "ok"}
