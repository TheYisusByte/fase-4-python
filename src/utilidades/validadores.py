# -*- coding: utf-8 -*-
# Módulo: utilidades/validadores.py
# Responsable: Juan Daniel Granados Torres  |  Rama: feature/excepciones-utilidades
# Lo usan: cliente.py y servicio.py para validar datos antes de crear objetos
"""
Funciones reutilizables de validación para Software FJ.

Convención del proyecto
  - Dato AUSENTE (None, texto vacío o solo espacios)
        -> lanza ParametroFaltanteError.
  - Dato PRESENTE pero INCORRECTO (formato, rango o tipo equivocado)
        -> lanza ValueError. La clase que invoca la función (Cliente,
           Servicio, etc.) captura ese ValueError y lo convierte en una
           excepción propia usando: raise ... from error
"""

import math
import re

from src.excepciones.errores import ParametroFaltanteError

# Patrones (expresiones regulares) definidos una sola vez.
# Letras (con tildes, ñ y ü); las palabras pueden separarse por espacio, apóstrofo o guion.
_PATRON_NOMBRE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
)
# usuario@dominio.extension
_PATRON_CORREO = re.compile(
    r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$"
)
# Un '+' opcional al inicio y luego solo dígitos.
_PATRON_TELEFONO = re.compile(r"^\+?\d+$")


def validar_texto(valor, campo="texto", longitud_minima=1, longitud_maxima=100):
    """Valida que 'valor' sea un texto con longitud permitida y lo devuelve sin espacios sobrantes."""
    if valor is None:
        raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio.")
    if not isinstance(valor, str):
        raise ValueError(f"El campo '{campo}' debe ser texto.")

    limpio = valor.strip()
    if limpio == "":
        raise ParametroFaltanteError(f"El campo '{campo}' no puede estar vacío.")
    if len(limpio) < longitud_minima:
        raise ValueError(
            f"El campo '{campo}' debe tener al menos {longitud_minima} caracteres."
        )
    if len(limpio) > longitud_maxima:
        raise ValueError(
            f"El campo '{campo}' no puede superar {longitud_maxima} caracteres."
        )
    return limpio


def validar_nombre_persona(valor, campo="nombre"):
    """Valida un nombre de persona: solo letras, espacios, apóstrofos y guiones."""
    limpio = validar_texto(valor, campo, longitud_minima=2, longitud_maxima=60)
    limpio = " ".join(limpio.split())  # convierte varios espacios seguidos en uno solo
    if not _PATRON_NOMBRE.match(limpio):
        raise ValueError(
            f"El campo '{campo}' solo puede contener letras, espacios, apóstrofos y guiones."
        )
    return limpio


def validar_correo(valor, campo="correo"):
    """Valida el formato de un correo electrónico y lo devuelve en minúsculas."""
    limpio = validar_texto(valor, campo, longitud_minima=6, longitud_maxima=100)
    if " " in limpio or ".." in limpio or not _PATRON_CORREO.match(limpio):
        raise ValueError(f"El correo '{limpio}' no tiene un formato válido.")
    return limpio.lower()


def validar_telefono(valor, campo="teléfono"):
    """Valida un teléfono: 7 a 15 dígitos, con '+' inicial opcional. Devuelve solo '+' y dígitos."""
    limpio = validar_texto(valor, campo, longitud_minima=7, longitud_maxima=25)
    # Se permiten espacios, guiones y paréntesis como adorno, pero se eliminan.
    for adorno in (" ", "-", "(", ")"):
        limpio = limpio.replace(adorno, "")
    if not _PATRON_TELEFONO.match(limpio):
        raise ValueError(
            f"El campo '{campo}' solo puede contener dígitos y un '+' inicial opcional."
        )
    cantidad_digitos = len(limpio.lstrip("+"))
    if not 7 <= cantidad_digitos <= 15:
        raise ValueError(f"El campo '{campo}' debe tener entre 7 y 15 dígitos.")
    return limpio


def validar_numero_positivo(valor, campo="valor", permitir_cero=False, solo_entero=False):
    """
    Valida que 'valor' sea un número (int o float) mayor que cero.
      - permitir_cero=True: también acepta 0 (útil para un depósito que puede ser 0).
      - solo_entero=True:   exige un número entero (útil para la capacidad de una sala).
    """
    if valor is None:
        raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio.")
    # bool es un tipo "hijo" de int en Python (True == 1), por eso se rechaza aparte.
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"El campo '{campo}' debe ser un número.")
    if not math.isfinite(valor):  # rechaza nan e infinito
        raise ValueError(f"El campo '{campo}' debe ser un número finito.")
    if solo_entero and not float(valor).is_integer():
        raise ValueError(f"El campo '{campo}' debe ser un número entero.")
    if permitir_cero:
        if valor < 0:
            raise ValueError(f"El campo '{campo}' no puede ser negativo.")
    elif valor <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor que cero.")
    return valor
