# -*- coding: utf-8 -*-
# Archivo: asesoria.py
# Clase AsesoriaEspecializada: servicio de asesoría. La tarifa por hora depende del nivel del asesor.
from src.excepciones.errores import ServicioInvalidoError
from src.modelos.servicio import Servicio
from src.utilidades.validadores import validar_numero_positivo, validar_texto


class AsesoriaEspecializada(Servicio):
    """Asesoría especializada. Se permite de 1 a 8 horas."""

    DURACION_MINIMA = 1
    DURACION_MAXIMA = 8
    # Diccionario con el multiplicador de la tarifa según el nivel del asesor
    MULTIPLICADORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, identificador, nombre, tarifa_hora_base, nivel="junior", disponible=True):
        super().__init__(identificador, nombre, disponible)
        try:
            self.__tarifa_hora_base = validar_numero_positivo(tarifa_hora_base, "tarifa base por hora")
            # Pasamos el nivel a minúsculas para aceptar "Senior", "SENIOR", etc.
            nivel_normalizado = validar_texto(nivel, "nivel", 3, 20).lower()
            if nivel_normalizado not in self.MULTIPLICADORES:
                opciones = ", ".join(self.MULTIPLICADORES)
                raise ValueError(f"nivel '{nivel}' no existe (opciones: {opciones}).")
            self.__nivel = nivel_normalizado
        except ValueError as error:
            raise ServicioInvalidoError(f"Datos de la asesoría inválidos: {error}") from error

    @property
    def tarifa_hora_base(self):
        return self.__tarifa_hora_base

    @property
    def nivel(self):
        return self.__nivel

    def validar_parametros(self, duracion):
        self._validar_rango_duracion(duracion, self.DURACION_MINIMA, self.DURACION_MAXIMA, "horas")

    def _costo_base(self, duracion):
        # Costo base = tarifa base x multiplicador del nivel x horas
        return self.__tarifa_hora_base * self.MULTIPLICADORES[self.__nivel] * duracion

    def describir(self):
        return (f"{super().describir()} - nivel {self.nivel}, "
                f"tarifa base ${self.tarifa_hora_base:,.0f}/hora")
