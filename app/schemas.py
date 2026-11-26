from pydantic import BaseModel, ConfigDict, Field


class ServicioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    duracion_min: int = Field(gt=0, le=480)
    precio: float = Field(ge=0)
    anticipo: float = Field(default=0, ge=0)


class ServicioRead(ServicioCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool

class ServicioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    duracion_min: int | None = Field(default=None, gt=0, le=480)
    precio: float | None = Field(default=None, ge=0)
    anticipo: float | None = Field(default=None, ge=0)
    activo: bool | None = None