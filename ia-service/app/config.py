"""Configuración del servicio leída de variables de entorno."""
import os

TOKEN = os.getenv("SGBH_IA_TOKEN", "")
RUTA_MODELOS = os.getenv("SGBH_RUTA_MODELOS", "/modelos")
