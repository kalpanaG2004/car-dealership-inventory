from typing import Any

from fastapi import APIRouter, Depends, status
from pymongo.database import Database

from app.database import get_database
from app.dependencies import get_current_user
from app.schemas import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    database: Database = Depends(get_database),
    _: dict[str, Any] = Depends(get_current_user),
) -> VehicleResponse:
    result = database.vehicles.insert_one(payload.model_dump())
    return VehicleResponse(id=str(result.inserted_id), **payload.model_dump())
