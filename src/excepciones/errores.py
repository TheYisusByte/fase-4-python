# -*- coding: utf-8 -*-
# Archivo: errores.py
# Jerarquía de excepciones personalizadas de Software FJ.
#
# Por qué una jerarquía: con una clase base común (ErrorSoftwareFJ) se puede capturar
# "cualquier error propio del sistema" con un solo except, y con las clases hijas se
# distingue cada tipo de problema (cliente, servicio, reserva, cálculo...).
#
#   ErrorSoftwareFJ
#   ├── ParametroFaltanteError   (además es ValueError, ver nota abajo)
#   ├── ClienteInvalidoError
#   ├── ServicioInvalidoError
#   ├── ServicioNoDisponibleError
#   ├── ReservaInvalidaError
#   ├── OperacionNoPermitidaError
#   ├── CalculoInconsistenteError
#   └── ErrorGestion


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema.

    Cada clase hija define su propio `codigo` (FJ-101 a FJ-107) como atributo de clase.
    El método __str__ arma el formato exigido por la guía (sección 4.1):
        "[CÓDIGO] mensaje"
    Así el mismo formato aparece al imprimir el error y en logs/eventos.log, sin que
    cada lugar del código tenga que acordarse de agregar el código a mano.
    """

    # Código por defecto para errores generales que no tengan uno propio.
    codigo = "FJ-100"

    def __init__(self, mensaje=""):
        # Se guarda el mensaje "limpio" (sin código) por si se necesita aparte.
        super().__init__(mensaje)
        self.mensaje = mensaje

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


class ParametroFaltanteError(ErrorSoftwareFJ, ValueError):
    """Dato ausente (None, texto vacío o solo espacios).

    NOTA IMPORTANTE: hereda también de ValueError a propósito. Las clases del modelo
    (Cliente, Servicio, Reserva...) hacen `except ValueError` para traducir los errores
    de los validadores a sus propias excepciones. Gracias a eso, un campo vacío sale
    como ClienteInvalidoError / ServicioInvalidoError y conserva el
    ParametroFaltanteError original en __cause__ (raise ... from), que es lo que
    comprueba test_cliente_sin_nombre.
    """

    codigo = "FJ-106"


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de un cliente incorrectos, o cliente inexistente/duplicado."""

    codigo = "FJ-101"


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos de un servicio incorrectos (tarifa, nivel, disponibilidad...)."""

    codigo = "FJ-102"


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio no existe, ya existe, no es de un tipo válido o no está disponible."""

    codigo = "FJ-103"


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Datos de una reserva incorrectos (identificador, duración fuera de rango...)."""

    codigo = "FJ-104"


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Cambio de estado que no se puede hacer (ej.: procesar una reserva cancelada)."""

    codigo = "FJ-105"


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Error al calcular un costo (descuento fuera de rango, impuesto negativo...)."""

    codigo = "FJ-107"


class ErrorGestion(ErrorSoftwareFJ):
    """Error general del GestorFJ; se usa para encadenar (raise ... from) la causa original."""