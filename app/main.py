from fastapi import FastAPI

from .routers import servicios

app = FastAPI(title="API de Citas", version="0.1.0")
app.include_router(servicios.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}