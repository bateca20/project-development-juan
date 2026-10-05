from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])

# Listar todas las habitaciones
@router.get("/", response_model=List[schemas.HabitacionOut])
def obtener_habitaciones(db: Session = Depends(get_db)):
    return db.query(models.Habitacion).all()

# Crear una nueva habitación (Solo Admin / Empleado)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.HabitacionOut)
def crear_habitacion(habitacion: schemas.HabitacionCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Habitacion).filter(models.Habitacion.numero == habitacion.numero).first()
    if existe:
        raise HTTPException(status_code=400, detail="El número de habitación ya existe")
    
    nueva_habitacion = models.Habitacion(**habitacion.dict())
    db.add(nueva_habitacion)
    db.commit()
    db.refresh(nueva_habitacion)
    return nueva_habitacion

# Cambiar estado de una habitación (DISPONIBLE, OCUPADA, MANTENIMIENTO)
@router.patch("/{habitacion_id}/estado", response_model=schemas.HabitacionOut)
def cambiar_estado_habitacion(habitacion_id: int, estado: str, db: Session = Depends(get_db)):
    habitacion = db.query(models.Habitacion).filter(models.Habitacion.id == habitacion_id).first()
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    
    habitacion.estado = estado.upper()
    db.commit()
    db.refresh(habitacion)
    return habitacion