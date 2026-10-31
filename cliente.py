# cliente.py
# Clase Cliente: datos personales encapsulados (atributos privados) y validados.
from entidades import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError
from registro_logs import registrar_evento


class Cliente(Entidad):
    contador = 0  # sirve para darle un id distinto a cada cliente

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        # Primero reviso que no falte ningun dato
        faltantes = []
        if nombre is None:
            faltantes.append("nombre")
        if documento is None:
            faltantes.append("documento")
        if correo is None:
            faltantes.append("correo")
        if telefono is None:
            faltantes.append("telefono")
        if len(faltantes) > 0:
            raise ParametroFaltanteError("Faltan datos del cliente: " + ", ".join(faltantes))

        Cliente.contador += 1
        super().__init__("CLI-" + str(Cliente.contador))

        # Atributos privados
        self.__nombre = ""
        self.__documento = ""
        self.__correo = ""
        self.__telefono = ""

        # Uso los setters para que se validen los datos
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        registrar_evento("Cliente creado: " + self._id + " - " + self.__nombre)

    # ----- nombre -----
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener minimo 3 letras")
        if not valor.replace(" ", "").isalpha():
            raise ClienteInvalidoError("El nombre solo puede tener letras")
        self.__nombre = valor.strip().title()

    # ----- documento -----
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        try:
            int(valor)
        except ValueError as e:
            # Encadenamiento de excepciones: guardo el error original con "from e"
            raise ClienteInvalidoError("El documento '" + str(valor) + "' debe ser numerico") from e
        if len(str(valor)) < 6 or len(str(valor)) > 10:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 10 digitos")
        self.__documento = str(valor)

    # ----- correo -----
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ClienteInvalidoError("Correo invalido: " + str(valor))
        self.__correo = valor.strip().lower()

    # ----- telefono -----
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) != 10:
            raise ClienteInvalidoError("El telefono debe tener 10 digitos")
        self.__telefono = str(valor)

    def describir(self):
        return self._id + " | " + self.__nombre + " | Doc: " + self.__documento + " | " + self.__correo
