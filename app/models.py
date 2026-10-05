from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, TIMESTAMP, Boolean, Date
from sqlalchemy.sql import func
from .database import Base

SCHEMA_NAME = "hotel"

class Rol(Base):
    __tablename__ = "roles"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    documento = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.roles.id"), nullable=False, default=3)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())


class TipoHabitacion(Base):
    __tablename__ = "tipo_habitacion"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    capacidad = Column(Integer, nullable=False)
    precio_noche = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text, nullable=True)


class Habitacion(Base):
    __tablename__ = "habitaciones"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(10), nullable=False, unique=True)
    estado = Column(String(20), nullable=False, default="DISPONIBLE")
    tipo_habitacion_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.tipo_habitacion.id"), nullable=False)


class Reserva(Base):
    __tablename__ = "reservas"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.usuarios.id"), nullable=False)
    habitacion_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.habitaciones.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())


class Estancia(Base):
    __tablename__ = "estancias"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.reservas.id"), nullable=False, unique=True)
    empleado_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.usuarios.id"), nullable=False)
    fecha_checkin = Column(TIMESTAMP, nullable=False, server_default=func.now())
    fecha_checkout = Column(TIMESTAMP, nullable=True)
    total_habitacion = Column(Numeric(10, 2), default=0.00)
    total_servicios = Column(Numeric(10, 2), default=0.00)
    total_pagado = Column(Numeric(10, 2), default=0.00)
    estado = Column(String(20), nullable=False, default="ACTIVA")


class Servicio(Base):
    __tablename__ = "servicios"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)


class ConsumoServicio(Base):
    __tablename__ = "consumos_servicio"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    estancia_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.estancias.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.servicios.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())


class Auditoria(Base):
    __tablename__ = "auditoria"
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    tabla_afectada = Column(String(50), nullable=False)
    operacion = Column(String(10), nullable=False)
    datos_anteriores = Column(Text, nullable=True)  # O usa JSON / JSONB de sqlalchemy.dialects.postgresql
    datos_nuevos = Column(Text, nullable=True)      # O usa JSON / JSONB de sqlalchemy.dialects.postgresql
    fecha = Column(TIMESTAMP, server_default=func.now())