from sqlalchemy import Boolean, Integer, Numeric, String
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