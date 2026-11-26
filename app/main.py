from fastapi import FastAPI
from .routers import citas, servicios


app = FastAPI(title="API de Citas", version="0.1.0")
app.include_router(servicios.router)
app.include_router(citas.router)

@app.get("/salud")
def salud():
    return {"estado": "ok"}