#   # -*- coding: utf-8 -*-
# Módulo: utilidades/logger.py
# Responsable: Juan Daniel Granados Torres  |  Rama: feature/excepciones-utilidades
# Lo usan: gestor_fj.py y main.py para registrar eventos y errores en logs/eventos.log
"""
logger.py - Gestión de eventos y errores de Software FJ.

Todo se guarda en logs/eventos.log (modo append: nunca borra lo anterior).
Cada línea tiene: fecha y hora | nivel | módulo | mensaje.
"""

import logging
from pathlib import Path

# Carpeta principal del proyecto (proyect4/): este archivo está en
# proyect4/src/utilidades/, así que subimos dos niveles con parents[2].
BASE_DIR = Path(__file__).resolve().parents[2]

# Rutas del registro, tal como las pide la guía.
RUTA_LOGS = BASE_DIR / "logs"
ARCHIVO_LOG = RUTA_LOGS / "eventos.log"

NOMBRE_LOGGER = "SoftwareFJ"


def obtener_logger():
    """Devuelve el logger del proyecto, listo para usar.

    - Crea la carpeta logs/ si no existe.
    - Escribe en modo append.
    - Evita manejadores duplicados (si se llama varias veces, no repite líneas).
    """
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(NOMBRE_LOGGER)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger


def describir_error(error):
    """Arma el texto de un error incluyendo su causa original (__cause__).

    Ejemplo de salida:
    ClienteInvalidoError: [FJ-101] Correo inválido <- causa: ValueError: formato incorrecto
    """
    texto = f"{type(error).__name__}: {error}"
    causa = error.__cause__
    while causa is not None:
        texto += f" <- causa: {type(causa).__name__}: {causa}"
        causa = causa.__cause__
    return texto


# Funciones de ayuda (las tuyas, conservadas). stacklevel=2 hace que el log
# muestre el módulo que llamó a la función y no siempre "logger".
def registrar_evento(mensaje):
    """Registra eventos importantes del sistema."""
    obtener_logger().info(mensaje, stacklevel=2)


def registrar_error(mensaje, error=None):
    """Registra un error; si se pasa la excepción, añade su cadena de causas."""
    if error is not None:
        mensaje = f"{mensaje} | {describir_error(error)}"
    obtener_logger().error(mensaje, stacklevel=2)


def registrar_advertencia(mensaje):
    """Registra situaciones que requieren atención."""
    obtener_logger().warning(mensaje, stacklevel=2)
