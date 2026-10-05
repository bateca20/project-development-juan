from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

# ----------------------------------------
# ESQUEMAS DE AUTENTICACIÓN Y ROLES
# ----------------------------------------

class RolOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    rol_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ----------------------------------------
# ESQUEMAS DE USUARIO (CLIENTE / EMPLEADO / ADMIN)
# ----------------------------------------

class UsuarioCreate(BaseModel):
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    password: str
    rol_id: int = 3  # Rol por defecto: CLIENTE (ID 3)

class UsuarioUpdateRol(BaseModel):
    rol_id: int  # Para que el Administrador cambie el rol (ej. de Cliente a Empleado)

class UsuarioOut(BaseModel):
    id: int
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    rol_id: int
    activo: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# ----------------------------------------
# ESQUEMAS DE HABITACIONES Y TIPOS
# ----------------------------------------

class TipoHabitacionOut(BaseModel):
    id: int
    nombre: str
    capacidad: int
    precio_noche: Decimal
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class HabitacionCreate(BaseModel):
    numero: str
    tipo_habitacion_id: int

class HabitacionOut(BaseModel):
    id: int
    numero: str
    estado: str  # DISPONIBLE, OCUPADA, MANTENIMIENTO
    tipo_habitacion_id: int
    tipo: Optional[TipoHabitacionOut] = None

    class Config:
        from_attributes = True

# ----------------------------------------
# ESQUEMAS DE RESERVAS Y DISPONIBILIDAD
# ----------------------------------------

class ConsultaDisponibilidad(BaseModel):
    fecha_inicio: date
    fecha_fin: date

class ReservaCreate(BaseModel):
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date
    cliente_id: Optional[int] = None  # Si lo crea el cliente toma su ID, si lo crea el empleado especifica el ID

class ReservaOut(BaseModel):
    id: int
    cliente_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: str  # PENDIENTE, CONFIRMADA, CANCELADA, FINALIZADA
    fecha_creacion: datetime
    habitacion: Optional[HabitacionOut] = None
    cliente: Optional[UsuarioOut] = None

    class Config:
        from_attributes = True

# ----------------------------------------
# ESQUEMAS DE RECEPCIÓN (CHECK-IN Y CHECK-OUT)
# ----------------------------------------

class CheckInRequest(BaseModel):
    reserva_id: int

class CheckOutResponse(BaseModel):
    estancia_id: int
    reserva_id: int
    fecha_checkin: datetime
    fecha_checkout: datetime
    total_habitacion: Decimal
    total_servicios: Decimal
    total_pagado: Decimal
    estado: str

    class Config:
        from_attributes = True

# ----------------------------------------
# ESQUEMAS DE SERVICIOS Y CONSUMOS
# ----------------------------------------

class ServicioOut(BaseModel):
    id: int
    nombre: str
    precio: Decimal
    descripcion: Optional[str] = None
    activo: bool

    class Config:
        from_attributes = True

class ConsumoServicioCreate(BaseModel):
    estancia_id: int
    servicio_id: int
    cantidad: int = 1