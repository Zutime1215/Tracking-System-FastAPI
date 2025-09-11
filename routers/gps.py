from fastapi import APIRouter, Depends, HTTPException
from models import Locations, Users, NewGpsRequest
from database import get_db, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix="/gps",
    tags=["gps"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


current_location = {
    "B31": {"lat": None, "lng": None, "timestamp": None, "shared_by": None},
    "B32": {"lat": None, "lng": None, "timestamp": None, "shared_by": None},
    "B33": {"lat": None, "lng": None, "timestamp": None, "shared_by": None},
    "L08": {"lat": None, "lng": None, "timestamp": None, "shared_by": None},
    "L06": {"lat": None, "lng": None, "timestamp": None, "shared_by": None},
    "L10": {"lat": None, "lng": None, "timestamp": None, "shared_by": None}
}


@router.get("/", status_code=status.HTTP_200_OK)
def read_all_current_locations(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    return current_location

@router.get("/{bus_id}", status_code=status.HTTP_200_OK)
def get_gps_by_bus_id(bus_id: str, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    return current_location[bus_id]

@router.post("/{bus_id}", status_code=status.HTTP_201_CREATED)
async def update_gps_by_bus_id(bus_id: str, gps_request: NewGpsRequest, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed man!")

    new_gps_data = gps_request.dict()
    new_gps_data['shared_by'] = "sirens"
    new_gps_data['bus_id'] = bus_id
    current_location[bus_id] = new_gps_data

    new_gps_data = Locations(**new_gps_data)
    db.add(new_gps_data)
    db.commit()