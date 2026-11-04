# -*- coding: utf-8 -*-
# Archivo: entidad_base.py
# Clase abstracta de la que heredan Cliente, Servicio y Reserva.
# Una clase abstracta no se puede instanciar directamente, solo sirve como molde.
from abc import ABC, abstractmethod

from src.utilidades.validadores import validar_texto


class EntidadBase(ABC):
    """Todas las entidades del sistema tienen un identificador que no se puede cambiar."""

    def __init__(self, identificador):
        # Atributo privado (doble guion bajo): solo se accede desde la propiedad de abajo.
        # Si el id está mal, validar_texto lanza una excepción y la clase hija la traduce.
        self.__identificador = validar_texto(identificador, "identificador", 3, 30)

    @property
    def identificador(self):
        # Solo hay getter (sin setter), entonces el id es de solo lectura
        return self.__identificador

    @abstractmethod
    def describir(self):
        # Método abstracto: cada clase hija DEBE implementarlo a su manera (polimorfismo)
        pass

    def __str__(self):
        # Cuando hacemos print(objeto) se usa la descripción de cada clase
        return self.describir()
