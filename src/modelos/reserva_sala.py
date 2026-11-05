# -*- coding: utf-8 -*-
# Archivo: reserva_sala.py
# Clase ReservaSala: servicio de reserva de salas. Se cobra por hora.
from src.excepciones.errores import ServicioInvalidoError
from src.modelos.servicio import Servicio
from src.utilidades.validadores import validar_numero_positivo


class ReservaSala(Servicio):
    """Sala que se puede reservar. Se permite de 1 a 12 horas."""

    # Constantes de la clase con el rango de horas permitido
    DURACION_MINIMA = 1
    DURACION_MAXIMA = 12

    def __init__(self, identificador, nombre, capacidad, tarifa_hora, disponible=True):
        # El constructor del padre valida id, nombre y disponibilidad
        super().__init__(identificador, nombre, disponible)
        try:
            self.__capacidad = validar_numero_positivo(capacidad, "capacidad", solo_entero=True)
            self.__tarifa_hora = validar_numero_positivo(tarifa_hora, "tarifa por hora")
        except ValueError as error:
            raise ServicioInvalidoError(f"Datos de la sala inválidos: {error}") from error

    @property
    def capacidad(self):
        return self.__capacidad

    @property
    def tarifa_hora(self):
        return self.__tarifa_hora

    def validar_parametros(self, duracion):
        # Usamos el método estático del padre con los límites de la sala
        self._validar_rango_duracion(duracion, self.DURACION_MINIMA, self.DURACION_MAXIMA, "horas")

    def _costo_base(self, duracion):
        # Costo base de la sala = tarifa por hora x horas
        return self.__tarifa_hora * duracion

    def describir(self):
        # super().describir() trae la descripción del padre y aquí le agregamos más datos
        return (f"{super().describir()} - capacidad {self.capacidad} personas, "
                f"${self.tarifa_hora:,.0f}/hora")
