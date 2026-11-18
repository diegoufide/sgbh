"""Puntos de acceso v1 (DN01, tabla «Puntos de acceso del servicio sgbh-ia»)."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.seguridad import validar_token

router = APIRouter(prefix="/v1", dependencies=[Depends(validar_token)])

TipoModelo = Literal["atrasos", "cotizaciones", "mensajes"]


class TareaEntrada(BaseModel):
    id_tarea: int
    prioridad: Literal["ALTA", "MEDIA", "BAJA"]
    dias_restantes: int
    carga_responsable: int = Field(ge=0)
    reprogramaciones: int = Field(ge=0)
    cambios_diseno: int = Field(ge=0)
    material_en_espera: bool


class SolicitudSugerencia(BaseModel):
    descripcion: str = Field(min_length=20)
    ancho: float | None = Field(default=None, gt=0)
    alto: float | None = Field(default=None, gt=0)


class MensajeEntrada(BaseModel):
    resumen: str = Field(min_length=1)


def _sin_modelo(tipo: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                         detail=f"No hay un modelo de {tipo} activo")


@router.post("/atrasos/predecir")
def predecir_atrasos(tareas: list[TareaEntrada]):
    raise _sin_modelo("atrasos")


@router.post("/cotizaciones/sugerir")
def sugerir_cotizacion(solicitud: SolicitudSugerencia):
    raise _sin_modelo("cotizaciones")


@router.post("/mensajes/clasificar")
def clasificar_mensaje(mensaje: MensajeEntrada):
    raise _sin_modelo("mensajes")


@router.get("/modelos/{tipo}")
def consultar_modelo(tipo: TipoModelo):
    return {"tipo": tipo, "versiones": [], "version_activa": None}
