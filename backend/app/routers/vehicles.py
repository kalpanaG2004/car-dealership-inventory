import re
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pymongo import ReturnDocument
from pymongo.database import Database

from app.database import get_database
from app.dependencies import get_current_user, require_admin
from app.schemas import InventoryChange, VehicleCreate, VehicleResponse, VehicleUpdate

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


def get_vehicle_or_404(database: Database, vehicle_id: str) -> dict[str, Any]:
    try:
        object_id = ObjectId(vehicle_id)
    except InvalidId as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found") from error

    vehicle = database.vehicles.find_one({"_id": object_id})
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


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


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: str,
    payload: VehicleUpdate,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> VehicleResponse:
    vehicle = get_vehicle_or_404(database, vehicle_id)
    update_fields = payload.model_dump(exclude_unset=True)
    if update_fields:
        vehicle = database.vehicles.find_one_and_update(
            {"_id": vehicle["_id"]},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER,
        )
    return serialize_vehicle(vehicle)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: str,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(require_admin),
) -> Response:
    vehicle = get_vehicle_or_404(database, vehicle_id)
    database.vehicles.delete_one({"_id": vehicle["_id"]})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{vehicle_id}/purchase", response_model=VehicleResponse)
def purchase_vehicle(
    vehicle_id: str,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> VehicleResponse:
    try:
        object_id = ObjectId(vehicle_id)
    except InvalidId as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found") from error

    vehicle = database.vehicles.find_one_and_update(
        {"_id": object_id, "quantity": {"$gt": 0}},
        {"$inc": {"quantity": -1}},
        return_document=ReturnDocument.AFTER,
    )
    if vehicle is None:
        if database.vehicles.find_one({"_id": object_id}) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vehicle is out of stock")

    return serialize_vehicle(vehicle)


@router.post("/{vehicle_id}/restock", response_model=VehicleResponse)
def restock_vehicle(
    vehicle_id: str,
    payload: InventoryChange,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(require_admin),
) -> VehicleResponse:
    vehicle = get_vehicle_or_404(database, vehicle_id)
    updated_vehicle = database.vehicles.find_one_and_update(
        {"_id": vehicle["_id"]},
        {"$inc": {"quantity": payload.amount}},
        return_document=ReturnDocument.AFTER,
    )
    return serialize_vehicle(updated_vehicle)
