from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/servicios", tags=["Servicios"])


@router.post("", response_model=schemas.ServicioRead, status_code=status.HTTP_201_CREATED)
def crear(data: schemas.ServicioCreate, db: Session = Depends(get_db)):
    existe = db.scalar(select(models.Servicio).where(models.Servicio.nombre == data.nombre))
    if existe:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un servicio con ese nombre")
    servicio = models.Servicio(**data.model_dump())
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio


@router.get("", response_model=list[schemas.ServicioRead])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.scalars(select(models.Servicio).offset(skip).limit(limit)).all()



@router.get("/{servicio_id}", response_model=schemas.ServicioRead)
def obtener(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Servicio no encontrado")
    return servicio


@router.delete("/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Servicio no encontrado")
    servicio.activo = False
    db.commit()

@router.patch("/{servicio_id}", response_model=schemas.ServicioRead)
def editar(servicio_id: int, data: schemas.ServicioUpdate, db: Session = Depends(get_db)):
    servicio = db.get(models.Servicio, servicio_id)
    if not servicio:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Servicio no encontrado")
    cambios = data.model_dump(exclude_unset=True)
    if "nombre" in cambios:
        repetido = db.scalar(
            select(models.Servicio).where(
                models.Servicio.nombre == cambios["nombre"],
                models.Servicio.id != servicio_id,
            )
        )
        if repetido:
            raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un servicio con ese nombre")
    for campo, valor in cambios.items():
        setattr(servicio, campo, valor)
    db.commit()
    db.refresh(servicio)
    return servicio
