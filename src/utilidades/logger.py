
#logger.py
#Aca encuentran la gestion de eventos y errores del sistema 

import logging
from pathlib import Path


#este es el directorio principal del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

#Aca se encuentra la carpeta donde se guardaran los registros
CARPETA_LOGS = BASE_DIR / "logs"
CARPETA_LOGS.mkdir(parents=True, exist_ok=True)

#estos seran los archivos de registro
ARCHIVO_LOG = CARPETA_LOGS / "software_fj.log"


#esta sera la configuracion del logger
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

#esto servira para que evitemos agregar manejadores duplicados
if not logger.handlers:

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    manejador = logging.FileHandler(
        ARCHIVO_LOG,
        encoding="utf-8"
    )

    manejador.setFormatter(formato)
    logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Registra eventos importantes del sistema."""
    logger.info(mensaje)


def registrar_error(mensaje, error=None):
    """Registra errores y excepciones del sistema."""

    if error is not None:
        logger.error(
            "%s | Detalle: %s",
            mensaje,
            str(error),
            exc_info=(
                type(error),
                error,
                error.__traceback__
            )
        )
    else:
        logger.error(mensaje)


def registrar_advertencia(mensaje):
    """Registra situaciones que requieren atencion."""
    logger.warning(mensaje)
