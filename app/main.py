from fastapi import FastAPI

app = FastAPI(title="API de Citas", version="0.1.0")


@app.get("/salud")
def salud():
    return {"estado": "ok"}