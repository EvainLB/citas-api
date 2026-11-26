from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


@router.post("", response_model=schemas.CitaRead, status_code=status.HTTP_201_CREATED)
def crear(data: schemas.CitaCreate, db: Session = Depends(get_db)):
    # 1. ¿Existen la clienta, la empleada y el servicio?
    cliente = db.get(models.Usuario, data.cliente_id)
    if not cliente or cliente.rol != "cliente":
        raise HTTPException(404, "Clienta no encontrada")
    empleado = db.get(models.Usuario, data.empleado_id)
    if not empleado or empleado.rol not in ("empleado", "admin"):
        raise HTTPException(404, "Empleada no encontrada")
    servicio = db.get(models.Servicio, data.servicio_id)
    if not servicio or not servicio.activo:
        raise HTTPException(404, "Servicio no disponible")

    # 2. No se agenda en el pasado
    if data.inicio <= datetime.now():
        raise HTTPException(422, "La cita debe ser en el futuro")

    # 3. El sistema calcula la hora de fin
    fin = data.inicio + timedelta(minutes=servicio.duracion_min)

    # 4. ¿Se empalma con otra cita de la misma empleada?
    empalme = db.scalars(
        select(models.Cita).where(
            models.Cita.empleado_id == data.empleado_id,
            models.Cita.estado != "cancelada",
            data.inicio < models.Cita.fin,
            fin > models.Cita.inicio,
        )
    ).first()
    if empalme:
        raise HTTPException(409, "La empleada ya tiene una cita en ese horario")

    # 5. ¿La empleada bloqueó ese horario?
    bloqueo = db.scalars(
        select(models.Bloqueo).where(
            models.Bloqueo.usuario_id == data.empleado_id,
            data.inicio < models.Bloqueo.fin,
            fin > models.Bloqueo.inicio,
        )
    ).first()
    if bloqueo:
        raise HTTPException(409, "La empleada no está disponible en ese horario")

    # 6. Guardar
    cita = models.Cita(**data.model_dump(), fin=fin)
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita