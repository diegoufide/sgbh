"""Aplicación FastAPI del servicio sgbh-ia."""
from fastapi import FastAPI

from app.api.rutas import router

app = FastAPI(title="SG Business Hub - Servicio de IA", version="0.1.0")
app.include_router(router)


@app.get("/salud")
def salud():
    return {"estado": "ok", "modelos_cargados": []}
