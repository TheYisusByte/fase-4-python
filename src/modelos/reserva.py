# -*- coding: utf-8 -*-
# Archivo: reserva.py
# Clase Reserva y Enum EstadoReserva.
# Una reserva une a un cliente con un servicio por una duración y maneja su estado.
from enum import Enum

from src.excepciones.errores import (
    CalculoInconsistenteError,
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from src.modelos.cliente import Cliente
from src.modelos.entidad_base import EntidadBase
from src.modelos.servicio import Servicio


class EstadoReserva(Enum):
    # Los 4 estados posibles de una reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"


class Reserva(EntidadBase):
    """Reserva de un servicio hecha por un cliente.

    Cambios de estado permitidos:
      PENDIENTE  -> CONFIRMADA o CANCELADA
      CONFIRMADA -> PROCESADA o CANCELADA
      PROCESADA y CANCELADA son estados finales (de ahí no se sale).
    """

    def __init__(self, identificador, cliente, servicio, duracion):
        try:
            super().__init__(identificador)
        except ValueError as error:
            raise ReservaInvalidaError(f"Identificador de reserva inválido: {error}") from error

        # Revisamos que realmente nos pasen un Cliente y un Servicio
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        # No se puede reservar un servicio que no está disponible
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        # Cada servicio sabe cuál es su rango de duración (polimorfismo)
        servicio.validar_parametros(duracion)

        # Atributos privados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = EstadoReserva.PENDIENTE  # toda reserva empieza pendiente
        self.__costo_total = None                # se calcula al procesar
        self.__intentos_proceso = 0              # cuántas veces se intentó procesar

    # Solo getters: desde afuera estos datos no se pueden modificar directamente
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    @property
    def intentos_proceso(self):
        return self.__intentos_proceso

    def confirmar(self):
        # Solo se puede confirmar si está pendiente
        if self.__estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.identificador}: estado {self.__estado.value}."
            )
        self.__estado = EstadoReserva.CONFIRMADA

    def cancelar(self):
        # Solo se puede cancelar si está pendiente o confirmada
        if self.__estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self.identificador}: estado {self.__estado.value}."
            )
        self.__estado = EstadoReserva.CANCELADA

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo final y pasa la reserva a PROCESADA."""
        # Solo se procesa si está confirmada
        if self.__estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva {self.identificador}: estado {self.__estado.value}."
            )
        try:
            # Intentamos calcular el costo
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)
        except ErrorSoftwareFJ:
            # Si ya es una excepción nuestra, la dejamos pasar igual (raise sin nada)
            raise
        except Exception as error:
            # Si es cualquier otro error, lo convertimos en CalculoInconsistenteError
            # y con "from" guardamos el error original (encadenamiento de excepciones)
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo de la reserva {self.identificador}: {error}"
            ) from error
        else:
            # El else se ejecuta solo si el try NO falló: guardamos el costo y cambiamos el estado
            self.__costo_total = costo
            self.__estado = EstadoReserva.PROCESADA
        finally:
            # El finally se ejecuta siempre, falle o no. Aquí contamos el intento.
            self.__intentos_proceso += 1
        return self.__costo_total

    def describir(self):
        costo = f", total ${self.__costo_total:,.2f}" if self.__costo_total is not None else ""
        return (f"Reserva {self.identificador} [{self.__estado.value}] - "
                f"{self.__cliente.nombre} -> {self.__servicio.nombre} x {self.__duracion}{costo}")
