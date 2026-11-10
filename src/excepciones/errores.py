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
    """Excepción base de todo el sistema."""


class ParametroFaltanteError(ErrorSoftwareFJ, ValueError):
    """Dato ausente (None, texto vacío o solo espacios).

    NOTA IMPORTANTE: hereda también de ValueError a propósito. Las clases del modelo
    (Cliente, Servicio, Reserva...) hacen `except ValueError` para traducir los errores
    de los validadores a sus propias excepciones. Si esta clase NO fuera un ValueError,
    un campo vacío se saltaría esa traducción y saldría como ParametroFaltanteError
    en vez de ClienteInvalidoError / ServicioInvalidoError.
    """


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de un cliente incorrectos, o cliente inexistente/duplicado."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos de un servicio incorrectos (tarifa, nivel, disponibilidad...)."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio no existe, ya existe, no es de un tipo válido o no está disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Datos de una reserva incorrectos (identificador, duración fuera de rango...)."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Cambio de estado que no se puede hacer (ej.: procesar una reserva cancelada)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Error al calcular un costo (descuento fuera de rango, impuesto negativo...)."""


class ErrorGestion(ErrorSoftwareFJ):
    """Error general del GestorFJ; se usa para encadenar (raise ... from) la causa original."""