from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import crud
from schemas import ReservationCreate, Reservation

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/reservations/", response_model=Reservation)
def create_reservation_endpoint(reservation: ReservationCreate):
    return crud.create_reservation(reservation.model_dump())

@app.get("/reservations/{reservation_id}", response_model=Reservation)
def read_reservation_endpoint(reservation_id: int):
    reservation = crud.get_reservation(reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.get("/reservations/", response_model=list[Reservation])
def read_reservations_endpoint(skip: int = 0, limit: int = 10):
    reservations = crud.get_reservations(skip=skip, limit=limit)
    return reservations

@app.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation_endpoint(reservation_id: int, reservation: ReservationCreate):
    updated_reservation = crud.update_reservation(reservation_id, reservation.model_dump())
    if updated_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated_reservation

@app.delete("/reservations/{reservation_id}")
def delete_reservation_endpoint(reservation_id: int):
    reservation = crud.delete_reservation(reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
