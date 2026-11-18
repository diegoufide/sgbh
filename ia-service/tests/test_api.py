from fastapi.testclient import TestClient

from app import config
from app.main import app

cliente = TestClient(app)


def test_salud_responde_ok():
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ok"


def test_rechaza_peticion_sin_token():
    config.TOKEN = "token-de-prueba"
    respuesta = cliente.post("/v1/mensajes/clasificar", json={"resumen": "Necesito cambiar el color"})
    assert respuesta.status_code == 401


def test_sin_modelo_activo_responde_503():
    config.TOKEN = "token-de-prueba"
    respuesta = cliente.post("/v1/mensajes/clasificar", json={"resumen": "Necesito cambiar el color"},
                             headers={"X-Api-Token": "token-de-prueba"})
    assert respuesta.status_code == 503


def test_valida_descripcion_minima_de_cotizacion():
    config.TOKEN = "token-de-prueba"
    respuesta = cliente.post("/v1/cotizaciones/sugerir", json={"descripcion": "corta"},
                             headers={"X-Api-Token": "token-de-prueba"})
    assert respuesta.status_code == 422
