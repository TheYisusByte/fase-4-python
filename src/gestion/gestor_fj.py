import logging

# encabezado de las importaciones y logger 

# exepciones personalizdas de cada uno de los integrantes 
# se describe un tipo de problema distintos 
from src.excepciones import (
    ErrorGestion,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)
from src.modelos import Cliente, Servicio, Reserva
    
logger = logging.getLogger("SoftwareFJ")

# la clase GestorFJ es la clase administradora 
class GestorFJ:
    #Administra clientes, servicios y reservas usando listas internas

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        logger.info("GestorFJ iniciado")

   
    # Consultas devuelven copias para proteger las listas internas
    # se utiliza para los atributos prividados y se encapsula la informacion

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    # definimos los metodos de busqueda  mediante un ciclo for para validar cliente, servicio, reserva
    def buscar_cliente(self, id_cliente):
        for cliente in self._clientes:
            if cliente.id == id_cliente:
                return cliente
        raise ClienteInvalidoError(f"No se econtro cliente con Id '{id_cliente}'")

    def buscar_servicio(self, id_servicio):
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise ServicioNoDisponibleError(f"Fallo no existe servicio con Id '{id_servicio}'")

    def buscar_reserva(self, id_reserva):
        for reserva in self._reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ReservaInvalidaError(f"Error no existe reserva con Id '{id_reserva}'")


    # Clientes
    # registro de clientes 
    def registrar_cliente(self, *args, **kwargs):
        #Crea un Cliente con los datos dados y lo agrega a la lista.

        #try/except/else/finally. Devuelve el cliente o None si hubo error.
    
        cliente = None
        try:
            cliente = Cliente(*args, **kwargs)  # las validaciones viven en Cliente
            if any(c.id == cliente.id for c in self._clientes):
                raise ClienteInvalidoError(f"Cliente '{cliente.id}' ya se encuentra registrado")
        except Exception as e:
            logger.error("Fallo el registro del cliente: %s", e)
            cliente = None
        else:
            self._clientes.append(cliente)
            logger.info("Cliente registrado: %s", cliente.id)
        finally:
            logger.debug("Fin de registrar_cliente (total clientes: %d)", len(self._clientes))
        return cliente

    
    # Servicios
    
    def registrar_servicio(self, clase_servicio, *args, **kwargs):
        #Crea un servicio (ReservaSala, AlquilerEquipo o AsesoriaEspecializada)
        servicio = None
        try:
            if not (isinstance(clase_servicio, type) and issubclass(clase_servicio, Servicio)):
                raise ServicioNoDisponibleError("El tipo de servicio no es valido")
            servicio = clase_servicio(*args, **kwargs)
            if any(s.id == servicio.id for s in self._servicios):
                raise ServicioNoDisponibleError(f"El servicio '{servicio.id}' ya existe")
        except Exception as e:
            logger.error("Creacion de servicio fallida: %s", e)
            servicio = None
        else:
            self._servicios.append(servicio)
            logger.info("Servicio registrado: %s", servicio.id)
        finally:
            logger.debug("Fin de registrar_servicio (total servicios: %d)", len(self._servicios))
        return servicio

    
    # Reservas
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        #Crea una reserva para un cliente y servicio existentes.

        #Usa encadenamiento de excepciones el error original queda como causa
        #del ErrorGestion que se registra en el log.
    
        reserva = None
        try:
            try:
                cliente = self.buscar_cliente(id_cliente)
                servicio = self.buscar_servicio(id_servicio)
                reserva = Reserva(cliente, servicio, duracion)
            except Exception as e:
                raise ErrorGestion("No fue posible crear la reserva") from e
        except ErrorGestion as e:
            logger.error("%s | causa: %r", e, e.__cause__)
            reserva = None
        else:
            self._reservas.append(reserva)
            logger.info("Reserva creada: %s (cliente %s, servicio %s)",
                        reserva.id, id_cliente, id_servicio)
        finally:
            logger.debug("Fin de crear_reserva (total reservas: %d)", len(self._reservas))
        return reserva

    def confirmar_reserva(self, id_reserva):
        return self._operar_reserva(id_reserva, "confirmar")

    def cancelar_reserva(self, id_reserva):
        return self._operar_reserva(id_reserva, "cancelar")

    def procesar_reserva(self, id_reserva):
        return self._operar_reserva(id_reserva, "procesar")

    def _operar_reserva(self, id_reserva, accion):
        #Ejecuta confirmar/cancelar/procesar de forma segura. Devuelve True/False
        try:
            reserva = self.buscar_reserva(id_reserva)
            if accion not in ("confirmar", "cancelar", "procesar"):
                raise OperacionNoPermitidaError(f"Accion '{accion}' no permitida")
            getattr(reserva, accion)()
        except Exception as e:
            logger.error("No se pudo %s la reserva '%s': %s", accion, id_reserva, e)
            return False
        else:
            logger.info("Reserva '%s': %s realizado", id_reserva, accion)
            return True
        finally:
            logger.debug("Fin de %s reserva", accion)


    # Resumen
    def resumen(self):
        return {
            "clientes": len(self._clientes),
            "servicios": len(self._servicios),
            "reservas": len(self._reservas),
        }
