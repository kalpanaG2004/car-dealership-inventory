import re
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from pymongo.database import Database

from app.database import get_database
from app.dependencies import get_current_user
from app.schemas import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


def serialize_vehicle(vehicle: dict[str, Any]) -> VehicleResponse:
    return VehicleResponse(
        id=str(vehicle["_id"]),
        make=vehicle["make"],
        model=vehicle["model"],
        category=vehicle["category"],
        price=vehicle["price"],
        quantity=vehicle["quantity"],
    )


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> VehicleResponse:
    result = database.vehicles.insert_one(payload.model_dump())
    return VehicleResponse(id=str(result.inserted_id), **payload.model_dump())


@router.get("", response_model=list[VehicleResponse])
def list_vehicles(
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> list[VehicleResponse]:
    return [serialize_vehicle(vehicle) for vehicle in database.vehicles.find({})]


@router.get("/search", response_model=list[VehicleResponse])
def search_vehicles(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, gt=0),
    max_price: float | None = Query(default=None, gt=0),
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> list[VehicleResponse]:
    filters: dict[str, Any] = {}
    for field, value in {"make": make, "model": model, "category": category}.items():
        if value:
            filters[field] = {"$regex": re.escape(value), "$options": "i"}

    if min_price is not None or max_price is not None:
        price_filter: dict[str, float] = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filters["price"] = price_filter

    return [serialize_vehicle(vehicle) for vehicle in database.vehicles.find(filters)]
