"""Valida el token compartido entre sgbh-web y sgbh-ia."""
from fastapi import Header, HTTPException, status

from app import config


def validar_token(x_api_token: str = Header(default="")) -> None:
    if not config.TOKEN or x_api_token != config.TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
