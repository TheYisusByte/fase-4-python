# -*- coding: utf-8 -*-
# Archivo: test_basico.py
# Pruebas automáticas de Software FJ con unittest (viene con Python, no se instala nada).
# Se ejecutan desde la carpeta principal del proyecto con:
#     python -m unittest discover -s tests -t .
# Responsable: Juan Daniel Granados Torres | Rama: feature/simulacion-pruebas-docs
# Cada método que empieza por "test_" es una prueba. Si no lanza ningún error, pasa.
import unittest

from src.excepciones.errores import (
    CalculoInconsistenteError,
    ClienteInvalidoError,
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from src.modelos.alquiler_equipo import AlquilerEquipo
from src.modelos.asesoria import AsesoriaEspecializada
from src.modelos.cliente import Cliente
from src.modelos.reserva import EstadoReserva, Reserva
from src.modelos.reserva_sala import ReservaSala
from src.modelos.servicio import Servicio
from src.utilidades.logger import describir_error
from src.utilidades.validadores import (
    validar_correo,
    validar_nombre_persona,
    validar_numero_positivo,
    validar_telefono,
    validar_texto,
)


class PruebasSoftwareFJ(unittest.TestCase):
    """Pruebas del dominio: clientes, servicios y reservas."""

    def setUp(self):
        # setUp se ejecuta ANTES de cada prueba: así cada una parte de datos limpios.
        self.cliente = Cliente("CLI-001", "Ana Gómez", "ana@correo.com", "3001234567")
        # Sala de 10 personas a $50.000 la hora
        self.sala = ReservaSala("SAL-001", "Sala Ejecutiva", 10, 50000)

    # ------------------------------------------------------------------
    # Las 6 pruebas que pide la guía
    # ------------------------------------------------------------------
    def test_correo_invalido(self):
        # assertRaises comprueba que el bloque lance EXACTAMENTE esa excepción.
        with self.assertRaises(ClienteInvalidoError):
            Cliente("CLI-002", "Luis Pérez", "correo-sin-arroba", "3001234567")

    def test_costo_con_impuesto_y_descuento(self):
        # 3 horas x $50.000 = 150.000 -> descuento 10 % = 135.000 -> IVA 19 % = 160.650
        costo = self.sala.calcular_costo(3, impuesto=0.19, descuento=0.10)
        self.assertAlmostEqual(costo, 160650.0, places=2)

    def test_costo_base_sin_extras(self):
        # 2 horas x $50.000 = 100.000 (sin impuesto ni descuento)
        self.assertEqual(self.sala.calcular_costo(2), 100000)

    def test_descuento_excesivo(self):
        # Un descuento de 150 % no tiene sentido: debe lanzar CalculoInconsistenteError
        with self.assertRaises(CalculoInconsistenteError):
            self.sala.calcular_costo(2, descuento=1.5)

    def test_cancelar_reserva_procesada(self):
        reserva = Reserva("RES-001", self.cliente, self.sala, 3)
        reserva.confirmar()
        reserva.procesar(0.19, 0.10)
        # PROCESADA es un estado final: ya no se puede cancelar
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_servicio_no_disponible(self):
        sala_cerrada = ReservaSala("SAL-002", "Sala Cerrada", 8, 40000, disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva("RES-002", self.cliente, sala_cerrada, 2)

    # ------------------------------------------------------------------
    # Pruebas adicionales (casos de la simulación y de POO)
    # ------------------------------------------------------------------
    def test_cliente_sin_nombre(self):
        # Dato AUSENTE (None): el validador lanza ParametroFaltanteError y Cliente
        # lo traduce a ClienteInvalidoError, conservando la causa original (raise ... from).
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente("CLI-003", None, "ana@correo.com", "3001234567")
        self.assertIsInstance(contexto.exception.__cause__, ParametroFaltanteError)

    def test_sala_con_capacidad_negativa(self):
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("SAL-003", "Sala Mala", -5, 50000)

    def test_duracion_invalida(self):
        # La sala permite de 1 a 12 horas; 20 está fuera del rango
        with self.assertRaises(ReservaInvalidaError):
            Reserva("RES-003", self.cliente, self.sala, 20)

    def test_reserva_exitosa_cambia_estado_y_guarda_costo(self):
        reserva = Reserva("RES-004", self.cliente, self.sala, 3)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)
        reserva.confirmar()
        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)
        total = reserva.procesar(0.19, 0.10)
        self.assertAlmostEqual(total, 160650.0, places=2)
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)
        self.assertEqual(reserva.costo_total, total)

    def test_alquiler_equipo_incluye_deposito(self):
        # 2 días x $30.000 + depósito $10.000 = 70.000
        equipo = AlquilerEquipo("EQU-001", "Proyector", 30000, deposito=10000)
        self.assertEqual(equipo.calcular_costo(2), 70000)

    def test_asesoria_senior_usa_multiplicador(self):
        # $40.000 x 1.5 (senior) x 2 horas = 120.000
        asesoria = AsesoriaEspecializada("ASE-001", "Asesoría Legal", 40000, "senior")
        self.assertEqual(asesoria.calcular_costo(2), 120000)

    def test_polimorfismo_describir(self):
        # Cada servicio describe a su manera, pero todos responden a describir()
        equipo = AlquilerEquipo("EQU-002", "Cámara", 25000)
        self.assertIn("capacidad", self.sala.describir())
        self.assertIn("depósito", equipo.describir())

    def test_servicio_es_abstracto(self):
        # Una clase abstracta no se puede instanciar directamente
        with self.assertRaises(TypeError):
            Servicio("SER-001", "Servicio genérico")

    def test_identificador_es_solo_lectura(self):
        # Encapsulación: el id solo tiene getter, asignarlo debe fallar
        with self.assertRaises(AttributeError):
            self.cliente.identificador = "OTRO-ID"

    def test_encadenamiento_conserva_causa_original(self):
        # raise ... from error: la causa original (ValueError) queda en __cause__
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente("CLI-004", "Luis Pérez", "correo-malo", "3001234567")
        self.assertIsInstance(contexto.exception.__cause__, ValueError)

    def test_formato_y_codigo_de_las_excepciones(self):
        # errores.py: formato "[CÓDIGO] mensaje" y código FJ-xxx de cada clase
        error = ClienteInvalidoError("prueba")
        self.assertEqual(str(error), "[FJ-101] prueba")
        self.assertEqual(error.codigo, "FJ-101")
        self.assertIsInstance(error, ErrorSoftwareFJ)
        self.assertEqual(CalculoInconsistenteError("x").codigo, "FJ-107")


class PruebasUtilidades(unittest.TestCase):
    """Pruebas de validadores.py y de describir_error() de logger.py."""

    def test_texto_vacio_es_parametro_faltante(self):
        with self.assertRaises(ParametroFaltanteError):
            validar_texto("   ", "nombre")
        with self.assertRaises(ParametroFaltanteError):
            validar_texto(None, "nombre")

    def test_nombre_se_limpia_y_se_valida(self):
        self.assertEqual(validar_nombre_persona("  María   José "), "María José")
        with self.assertRaises(ValueError):
            validar_nombre_persona("Ana123")

    def test_correo(self):
        self.assertEqual(validar_correo("Ana@Correo.COM"), "ana@correo.com")
        with self.assertRaises(ValueError):
            validar_correo("ana@correo")

    def test_telefono(self):
        self.assertEqual(validar_telefono("+57 (300) 123-4567"), "+573001234567")
        with self.assertRaises(ValueError):
            validar_telefono("123")

    def test_numero_positivo(self):
        self.assertEqual(validar_numero_positivo(50000), 50000)
        self.assertEqual(validar_numero_positivo(0, permitir_cero=True), 0)
        with self.assertRaises(ValueError):
            validar_numero_positivo(-5)
        with self.assertRaises(ValueError):
            validar_numero_positivo(True)  # un bool no cuenta como número
        with self.assertRaises(ValueError):
            validar_numero_positivo(10.5, solo_entero=True)

    def test_describir_error_incluye_causa_original(self):
        try:
            try:
                int("abc")
            except ValueError as causa:
                raise ClienteInvalidoError("Dato inválido") from causa
        except ClienteInvalidoError as error:
            texto = describir_error(error)
        self.assertIn("ClienteInvalidoError", texto)
        self.assertIn("causa: ValueError", texto)


if __name__ == "__main__":
    unittest.main()