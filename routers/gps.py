from fastapi import APIRouter, Depends, HTTPException
from models import Locations, Users, NewGpsRequest
from database import get_db, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from time import time
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



window_start = (int(time()) // 5) * 5 + 1
window_duration = 4
window_end = window_start + window_duration
buffer = []

def push_to_db():
    global buffer, current_location
    print(buffer)

@router.post("/{bus_id}", status_code=status.HTTP_201_CREATED)
async def update_gps_by_bus_id(bus_id: str, gps_request: NewGpsRequest, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed man!")

    global window_start, window_end, buffer
    new_gps_data = gps_request.dict()

    if new_gps_data['timestamp'] < window_start:
        raise HTTPException(status_code=400, detail="Request timestamp is old.")

    new_gps_data['shared_by'] = user.get('username')
    new_gps_data['bus_id'] = bus_id

    if new_gps_data['timestamp'] >= window_start and new_gps_data['timestamp'] <= window_end:
        buffer.append(new_gps_data)

    if new_gps_data['timestamp'] > window_end:
        push_to_db()

        buffer.clear()
        window_start = (int(new_gps_data['timestamp']) // 5) * 5 + 1
        window_end = window_start + window_duration
        print("window ", window_start, window_end)
        buffer.append(new_gps_data)


    # current_location[bus_id] = new_gps_data
    # new_gps_data = Locations(**new_gps_data)
    # db.add(new_gps_data)
    # db.commit()