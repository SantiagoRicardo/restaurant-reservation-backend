from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db=db, reservation=reservation)

@app.get("/reservations/", response_model=list[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations

@app.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = crud.update_reservation(db, reservation_id=reservation_id, reservation=reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@app.delete("/reservations/{reservation_id}", response_model=schemas.Reservation)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.delete_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation
