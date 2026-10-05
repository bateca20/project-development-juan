from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Consultar reservas
@router.get("/", response_model=List[schemas.ReservaOut])
def obtener_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()

# Crear Reserva con validación básica de fechas
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReservaOut)
def crear_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    if reserva.fecha_fin <= reserva.fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha de salida debe ser posterior a la de entrada")

    # Verificar si la habitación ya está ocupada/reservada en esas fechas
    solapada = db.query(models.Reserva).filter(
        models.Reserva.habitacion_id == reserva.habitacion_id,
        models.Reserva.estado.in_(["PENDIENTE", "CONFIRMADA"]),
        models.Reserva.fecha_inicio < reserva.fecha_fin,
        models.Reserva.fecha_fin > reserva.fecha_inicio
    ).first()

    if solapada:
        raise HTTPException(status_code=400, detail="La habitación no está disponible para el rango de fechas seleccionado")

    nueva_reserva = models.Reserva(**reserva.dict())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva