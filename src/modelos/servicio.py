# -*- coding: utf-8 -*-
# Archivo: servicio.py
# Clase abstracta Servicio. Es el padre de ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
# Aquí está el cálculo del costo, que es igual para todos los servicios.
from abc import abstractmethod

from src.excepciones.errores import (
    CalculoInconsistenteError,
    ReservaInvalidaError,
    ServicioInvalidoError,
)
from src.modelos.entidad_base import EntidadBase
from src.utilidades.validadores import validar_texto


class Servicio(EntidadBase):
    """Servicio que ofrece la empresa. Es abstracto, no se crea directamente."""

    def __init__(self, identificador, nombre, disponible=True):
        try:
            super().__init__(identificador)
            self.__nombre = validar_texto(nombre, "nombre del servicio", 3, 80)
        except ValueError as error:
            raise ServicioInvalidoError(f"Datos del servicio inválidos: {error}") from error
        # Usamos el setter para validar que sea True o False
        self.disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = valor

    # ---------- métodos abstractos: cada servicio los implementa a su manera ----------
    @abstractmethod
    def _costo_base(self, duracion):
        """Costo sin descuento ni impuesto."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        """Revisa que la duración esté dentro de lo permitido para ese servicio."""
        pass

    # ---------- método común a todos los servicios ----------
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """Calcula el costo total.

        Python no tiene sobrecarga de métodos como Java, entonces la simulamos con
        parámetros opcionales: se puede llamar solo con la duración, o con impuesto y/o descuento.

        Orden del cálculo: costo base -> se aplica el descuento -> se aplica el impuesto.
        El impuesto y el descuento van como fracción (0.19 = 19 %, 0.10 = 10 %).
        """
        # Primero revisamos que la duración sea válida
        self.validar_parametros(duracion)

        # Revisamos que descuento e impuesto sean números y tengan sentido
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise CalculoInconsistenteError("El descuento debe ser numérico.")
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise CalculoInconsistenteError("El impuesto debe ser numérico.")
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                f"El descuento debe estar entre 0 % y 100 % (recibido: {descuento * 100:.0f} %)."
            )
        if impuesto < 0:
            raise CalculoInconsistenteError("El impuesto no puede ser negativo.")

        # Cálculo en el orden pedido en la guía
        base = self._costo_base(duracion)
        con_descuento = base * (1 - descuento)
        total = con_descuento * (1 + impuesto)
        # round para evitar decimales raros de los float
        return round(total, 2)

    @staticmethod
    def _validar_rango_duracion(duracion, minimo, maximo, unidad):
        """Método estático (no usa self): revisa que la duración sea entera y esté en el rango."""
        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise ReservaInvalidaError(f"La duración debe ser un número entero de {unidad}.")
        if not minimo <= duracion <= maximo:
            raise ReservaInvalidaError(
                f"La duración debe estar entre {minimo} y {maximo} {unidad} (recibido: {duracion})."
            )

    def describir(self):
        # type(self).__name__ nos da el nombre de la clase real (ReservaSala, etc.)
        estado = "disponible" if self.disponible else "NO disponible"
        return f"{type(self).__name__} {self.identificador} '{self.nombre}' ({estado})"
