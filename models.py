from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from pydantic import BaseModel

class Locations(Base):
    __tablename__ = 'current_location'

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    timestamp = Column(Float)
    bus_id = Column(Integer)
    shared_by = Column(String, ForeignKey('users.username'))

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class NewGpsRequest(BaseModel):
    lat: float
    lng: float
    timestamp: float

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str