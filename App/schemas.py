from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    rol: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    rol: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ReservationBase(BaseModel):
    customer_name: str
    reservation_datetime: datetime
    age: int
    status: str = "activa"

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    total_cost: float
    id_reservation: str

    class Config:
        orm_mode = True
