# -*- coding: utf-8 -*-
# Convierte la carpeta en paquete y reexporta las excepciones, para poder escribir:
#   from src.excepciones import ClienteInvalidoError
from .errores import (
    CalculoInconsistenteError,
    ClienteInvalidoError,
    ErrorGestion,
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)

__all__ = [
    "CalculoInconsistenteError",
    "ClienteInvalidoError",
    "ErrorGestion",
    "ErrorSoftwareFJ",
    "OperacionNoPermitidaError",
    "ParametroFaltanteError",
    "ReservaInvalidaError",
    "ServicioInvalidoError",
    "ServicioNoDisponibleError",
]