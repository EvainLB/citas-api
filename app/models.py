from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Servicio(Base):
    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    duracion_min: Mapped[int] = mapped_column(Integer)
    precio: Mapped[float] = mapped_column(Numeric(10, 2))
    anticipo: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)   # no se puede repetir 
    password_hash: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(20), default="cliente")  # ¿qué rol por defecto?
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    telegram_chat_id: Mapped[str | None] = mapped_column(String(50))   # es opcional
    telefono: Mapped[str | None] = mapped_column(String(20), unique=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Cita(Base):
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id:  Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicios.id")) 
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    notas: Mapped[str | None] = mapped_column(String (500))
    anticipo_pagado: Mapped[bool] = mapped_column(Boolean, default=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Bloqueo(Base):
    __tablename__ = "bloqueos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    motivo: Mapped[str | None] = mapped_column(String (200))


