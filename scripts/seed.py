import secrets

from argon2 import PasswordHasher
from sqlalchemy import select

from app import models
from app.database import SessionLocal

ph = PasswordHasher()

USUARIAS = [
    ("duena@example.com", "Dueña Demo", "admin"),
    ("empleada@example.com", "Empleada Demo", "empleado"),
    ("clienta@example.com", "Clienta Demo", "cliente"),
]

db = SessionLocal()
for email, nombre, rol in USUARIAS:
    if db.scalar(select(models.Usuario).where(models.Usuario.email == email)):
        continue
    db.add(models.Usuario(
        email=email,
        nombre=nombre,
        rol=rol,
        password_hash=ph.hash(secrets.token_urlsafe(16)),
    ))
db.commit()
for u in db.scalars(select(models.Usuario)):
    print(u.id, u.nombre, u.rol)
db.close()