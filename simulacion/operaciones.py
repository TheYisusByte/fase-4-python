# Archivo: operaciones.py
# Simulación de 12 operaciones del sistema Software FJ.
#
# Objetivo: demostrar, sin interfaz gráfica ni base de datos, que el sistema funciona con
# datos VÁLIDOS y que se mantiene estable ante datos INVÁLIDOS (los errores se capturan,
# se registran en logs/eventos.log y la ejecución continúa).
#
# Buenas prácticas aplicadas en este archivo:
#   - Cada operación es una función pequeña con una sola responsabilidad.
#   - El estado compartido entre operaciones (por ejemplo, las reservas creadas) viaja en
#     un diccionario "contexto", en lugar de variables globales.
#   - Un "envoltorio" (_ejecutar_operacion) captura cualquier error inesperado para que
#     una operación fallida NUNCA detenga la simulación completa.
#   - Los montos esperados están comentados con su cálculo para poder verificarlos a mano.

from src.modelos.alquiler_equipo import AlquilerEquipo
from src.modelos.asesoria import AsesoriaEspecializada
from src.modelos.reserva_sala import ReservaSala
from src.utilidades.logger import registrar_error, registrar_evento


# --------------------------------------------------------------------------------------
# Utilidades de presentación
# --------------------------------------------------------------------------------------
def _mostrar(texto):
    """Imprime una línea con sangría para que la salida sea fácil de leer."""
    print(f"    {texto}")


def _resultado(exito, texto):
    """Muestra un resultado con un marcador claro (OK o FALLO)."""
    marcador = "OK   " if exito else "FALLO"
    _mostrar(f"[{marcador}] {texto}")


def _esperado_none(objeto, texto_exito, texto_fallo):
    """Para operaciones del gestor que devuelven None cuando algo sale mal.

    Se usa tanto en los casos válidos como en los inválidos: lo importante es mostrar
    qué devolvió el gestor, no asumir el resultado.
    """
    if objeto is None:
        _resultado(False, texto_fallo)
    else:
        _resultado(True, texto_exito)


# --------------------------------------------------------------------------------------
# Las 12 operaciones
# --------------------------------------------------------------------------------------
def _op01_cliente_valido(gestor, contexto):
    """Operación 1: registrar un cliente con datos correctos."""
    cliente = gestor.registrar_cliente(
        "CLI-001", "Laura Pérez", "laura.perez@correo.com", "+57 300 123 4567")
    _esperado_none(cliente, "Cliente registrado correctamente.", "No se pudo registrar el cliente.")


def _op02_segundo_cliente_valido(gestor, contexto):
    """Operación 2: registrar un segundo cliente (nombre con tilde y apóstrofo)."""
    cliente = gestor.registrar_cliente(
        "CLI-002", "Carlos O'Brien", "carlos.obrien@correo.com", "3101234567")
    _esperado_none(cliente, "Cliente registrado correctamente.", "No se pudo registrar el cliente.")


def _op03_cliente_correo_invalido(gestor, contexto):
    """Operación 3: ERROR esperado. El correo no tiene arroba."""
    cliente = gestor.registrar_cliente(
        "CLI-003", "Ana Gómez", "correo-sin-arroba", "3201234567")
    _esperado_none(cliente, "Cliente registrado (inesperado).",
                   "Rechazado como se esperaba: correo con formato inválido.")


def _op04_cliente_duplicado(gestor, contexto):
    """Operación 4: ERROR esperado. Se repite el identificador CLI-001."""
    cliente = gestor.registrar_cliente(
        "CLI-001", "Otra Persona", "otra.persona@correo.com", "3001112233")
    _esperado_none(cliente, "Cliente registrado (inesperado).",
                   "Rechazado como se esperaba: identificador duplicado.")


def _op05_servicios_validos(gestor, contexto):
    """Operación 5: registrar los tres tipos de servicio (polimorfismo) y uno no disponible."""
    servicios = [
        # (clase, argumentos posicionales, argumentos con nombre)
        (ReservaSala, ("SAL-001", "Sala de juntas", 12, 50000), {}),
        (AlquilerEquipo, ("EQP-001", "Proyector HD", 30000, 100000), {}),
        (AsesoriaEspecializada, ("ASE-001", "Asesoría en arquitectura de software", 80000),
         {"nivel": "Senior"}),  # "Senior" con mayúscula: el sistema lo normaliza
        # Servicio válido pero marcado como no disponible; se usará en la operación 9.
        (AlquilerEquipo, ("EQP-002", "Cámara 4K", 45000, 150000), {"disponible": False}),
    ]
    for clase, args, kwargs in servicios:
        servicio = gestor.registrar_servicio(clase, *args, **kwargs)
        _esperado_none(servicio, servicio.describir() if servicio else "",
                       f"No se pudo registrar {args[0]}.")


def _op06_servicios_invalidos(gestor, contexto):
    """Operación 6: ERRORES esperados al registrar servicios con datos incorrectos."""
    casos = [
        ("nivel de asesor inexistente",
         AsesoriaEspecializada, ("ASE-002", "Asesoría contable", 90000), {"nivel": "maestro"}),
        ("capacidad igual a cero",
         ReservaSala, ("SAL-002", "Sala pequeña", 0, 40000), {}),
        ("tipo de servicio que no es una clase Servicio",
         str, ("XXX-001", "Falso", 1), {}),
    ]
    for descripcion, clase, args, kwargs in casos:
        servicio = gestor.registrar_servicio(clase, *args, **kwargs)
        _esperado_none(servicio, f"Registrado (inesperado): {descripcion}.",
                       f"Rechazado como se esperaba: {descripcion}.")


def _op07_reservas_validas(gestor, contexto):
    """Operación 7: crear tres reservas válidas, una por cada tipo de servicio."""
    reservas = [
        ("sala", "CLI-001", "SAL-001", 4),       # 4 horas (rango 1 a 12)
        ("equipo", "CLI-002", "EQP-001", 3),     # 3 días  (rango 1 a 30)
        ("asesoria", "CLI-001", "ASE-001", 3),   # 3 horas (rango 1 a 8)
    ]
    for clave, id_cliente, id_servicio, duracion in reservas:
        reserva = gestor.crear_reserva(id_cliente, id_servicio, duracion)
        # Se guarda la reserva en el contexto para usarla en operaciones posteriores.
        contexto[clave] = reserva
        _esperado_none(reserva, reserva.describir() if reserva else "",
                       f"No se pudo crear la reserva de {clave}.")


def _op08_duracion_invalida(gestor, contexto):
    """Operación 8: ERRORES esperados por duración fuera de rango o de tipo incorrecto."""
    casos = [
        ("sala por 15 horas (máximo 12)", "SAL-001", 15),
        ("equipo por 0 días (mínimo 1)", "EQP-001", 0),
        ("asesoría por 2.5 horas (debe ser entero)", "ASE-001", 2.5),
    ]
    for descripcion, id_servicio, duracion in casos:
        reserva = gestor.crear_reserva("CLI-001", id_servicio, duracion)
        _esperado_none(reserva, f"Reserva creada (inesperado): {descripcion}.",
                       f"Rechazada como se esperaba: {descripcion}.")


def _op09_cliente_o_servicio_invalido(gestor, contexto):
    """Operación 9: ERRORES esperados por cliente/servicio inexistente o no disponible."""
    casos = [
        ("cliente inexistente (CLI-999)", "CLI-999", "SAL-001"),
        ("servicio inexistente (SAL-999)", "CLI-001", "SAL-999"),
        ("servicio no disponible (EQP-002)", "CLI-001", "EQP-002"),
    ]
    for descripcion, id_cliente, id_servicio in casos:
        reserva = gestor.crear_reserva(id_cliente, id_servicio, 1)
        _esperado_none(reserva, f"Reserva creada (inesperado): {descripcion}.",
                       f"Rechazada como se esperaba: {descripcion}.")


def _op10_confirmar_y_procesar(gestor, contexto):
    """Operación 10: flujo completo PENDIENTE -> CONFIRMADA -> PROCESADA con impuesto y descuento.

    Cálculo esperado para la sala (4 horas x $50.000, descuento 10 %, impuesto 19 %):
        base      = 50.000 x 4          = 200.000
        descuento = 200.000 x (1 - 0,10) = 180.000
        total     = 180.000 x (1 + 0,19) = 214.200,00
    """
    reserva = contexto["sala"]
    confirmada = gestor.confirmar_reserva(reserva.identificador)
    _resultado(confirmada, f"Confirmación de {reserva.identificador}: estado {reserva.estado.value}.")
    procesada = gestor.procesar_reserva(reserva.identificador, impuesto=0.19, descuento=0.10)
    _resultado(procesada, f"Proceso de {reserva.identificador}: total ${reserva.costo_total:,.2f} "
                          f"(esperado $214,200.00), estado {reserva.estado.value}.")


def _op11_calculo_invalido_y_reintento(gestor, contexto):
    """Operación 11: un cálculo inválido NO cambia el estado y la reserva se puede reintentar.

    Primero se procesa con un descuento imposible (150 %): falla y la reserva sigue
    CONFIRMADA. Luego se reintenta con un descuento válido del 5 %.
    Cálculo esperado para la asesoría (3 h x $80.000 x 1,5 nivel senior):
        base      = 80.000 x 1,5 x 3        = 360.000
        descuento = 360.000 x (1 - 0,05)    = 342.000
        total     = 342.000 x (1 + 0,19)    = 406.980,00
    """
    reserva = contexto["asesoria"]
    gestor.confirmar_reserva(reserva.identificador)

    fallo = gestor.procesar_reserva(reserva.identificador, impuesto=0.19, descuento=1.5)
    _resultado(not fallo, f"Descuento del 150 % rechazado; estado sigue {reserva.estado.value}, "
                          f"intentos de proceso: {reserva.intentos_proceso}.")

    exito = gestor.procesar_reserva(reserva.identificador, impuesto=0.19, descuento=0.05)
    _resultado(exito, f"Reintento correcto: total ${reserva.costo_total:,.2f} "
                      f"(esperado $406,980.00), intentos de proceso: {reserva.intentos_proceso}.")


def _op12_cancelar_y_operar_cancelada(gestor, contexto):
    """Operación 12: cancelar una reserva y comprobar que un estado final no permite más cambios."""
    reserva = contexto["equipo"]
    cancelada = gestor.cancelar_reserva(reserva.identificador)
    _resultado(cancelada, f"Cancelación de {reserva.identificador}: estado {reserva.estado.value}.")

    # CANCELADA es un estado final: confirmar y procesar deben ser rechazados (devuelven False).
    confirmar = gestor.confirmar_reserva(reserva.identificador)
    _resultado(not confirmar, "Confirmar una reserva cancelada fue rechazado, como se esperaba.")
    procesar = gestor.procesar_reserva(reserva.identificador)
    _resultado(not procesar, "Procesar una reserva cancelada fue rechazado, como se esperaba.")


# Lista ordenada de operaciones: (título, función). Agregar una operación nueva es
# tan simple como añadir una línea aquí.
OPERACIONES = [
    ("Registrar cliente válido", _op01_cliente_valido),
    ("Registrar segundo cliente válido", _op02_segundo_cliente_valido),
    ("Registrar cliente con correo inválido", _op03_cliente_correo_invalido),
    ("Registrar cliente duplicado", _op04_cliente_duplicado),
    ("Registrar servicios válidos (sala, equipo, asesoría)", _op05_servicios_validos),
    ("Registrar servicios con datos inválidos", _op06_servicios_invalidos),
    ("Crear reservas válidas", _op07_reservas_validas),
    ("Crear reservas con duración inválida", _op08_duracion_invalida),
    ("Crear reservas con cliente/servicio inválido", _op09_cliente_o_servicio_invalido),
    ("Confirmar y procesar con impuesto y descuento", _op10_confirmar_y_procesar),
    ("Cálculo inválido y reintento", _op11_calculo_invalido_y_reintento),
    ("Cancelar y operar sobre un estado final", _op12_cancelar_y_operar_cancelada),
]


def _ejecutar_operacion(numero, titulo, funcion, gestor, contexto):
    """Ejecuta una operación aislándola: si algo inesperado falla, se registra y se continúa.

    Aquí SÍ se captura Exception de forma amplia porque es el último nivel de defensa de
    la simulación: el gestor ya maneja los errores esperados del negocio.
    """
    print(f"\n[{numero:02d}] {titulo}")
    registrar_evento(f"Simulación - operación {numero}: {titulo}")
    try:
        funcion(gestor, contexto)
    except Exception as error:
        _resultado(False, f"Error inesperado en la operación: {error}")
        registrar_error(f"Error inesperado en la operación {numero}", error)


def ejecutar_simulacion(gestor):
    """Corre las 12 operaciones en orden y muestra un resumen final."""
    print("=" * 70)
    print("SIMULACIÓN SOFTWARE FJ - 12 operaciones")
    print("=" * 70)
    registrar_evento("Inicio de la simulación")

    contexto = {}  # estado compartido entre operaciones (reservas creadas, etc.)
    for numero, (titulo, funcion) in enumerate(OPERACIONES, start=1):
        _ejecutar_operacion(numero, titulo, funcion, gestor, contexto)

    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    for nombre, cantidad in gestor.resumen().items():
        print(f"  {nombre.capitalize()}: {cantidad}")
    print("\n  Estado de las reservas:")
    for reserva in gestor.reservas:
        print(f"    {reserva.describir()}")
    registrar_evento("Fin de la simulación")