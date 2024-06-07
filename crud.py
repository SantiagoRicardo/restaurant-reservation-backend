# crud.py

from sqlalchemy.orm import Session
import models, schemas

def get_reservations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Reservation).offset(skip).limit(limit).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationCreate):
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        for key, value in reservation.dict().items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation
