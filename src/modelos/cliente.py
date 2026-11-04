# -*- coding: utf-8 -*-
# Archivo: cliente.py
# Clase Cliente: representa a la persona que hace las reservas.
from src.excepciones.errores import ClienteInvalidoError
from src.modelos.entidad_base import EntidadBase
from src.utilidades.validadores import (
    validar_correo,
    validar_nombre_persona,
    validar_telefono,
)


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos son privados y se validan cada vez que se asignan."""

    def __init__(self, identificador, nombre, correo, telefono):
        # Primero el constructor del padre, que valida el identificador.
        # Si lanza ValueError, lo convertimos en ClienteInvalidoError con "from"
        # para no perder la causa original.
        try:
            super().__init__(identificador)
        except ValueError as error:
            raise ClienteInvalidoError(f"Identificador de cliente inválido: {error}") from error

        # Estas asignaciones pasan por los setters de abajo, que validan cada dato
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        try:
            self.__nombre = validar_nombre_persona(valor)
        except ValueError as error:
            # Traducimos el ValueError a nuestra excepción propia
            raise ClienteInvalidoError(f"Nombre inválido: {error}") from error

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        try:
            self.__correo = validar_correo(valor)
        except ValueError as error:
            raise ClienteInvalidoError(f"Correo inválido: {error}") from error

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        try:
            self.__telefono = validar_telefono(valor)
        except ValueError as error:
            raise ClienteInvalidoError(f"Teléfono inválido: {error}") from error

    def describir(self):
        # Implementación del método abstracto de EntidadBase
        return (f"Cliente {self.identificador}: {self.nombre} "
                f"<{self.correo}> Tel. {self.telefono}")

