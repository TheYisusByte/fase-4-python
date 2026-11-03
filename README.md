# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto académico (UNAD - Programación 213023, Fase 4). Aplicación en Python orientada a objetos,
**sin base de datos**: los datos viven en listas internas y solo se escriben archivos para el registro de eventos y errores.

## Integrantes
| N.º | Nombre | Módulos a cargo |
|---|---|---|
| 1 | (completar) | excepciones, utilidades |
| 2 | (completar) | entidad_base, cliente |
| 3 | (completar) | servicio y servicios derivados |
| 4 | (completar) | reserva, gestor |
| 5 | (completar) | simulación, pruebas, documentación |

## Requisitos
- Python 3.8 o superior (no requiere instalar librerías externas).

## Ejecución
```
python main.py                                  # simulación de 12 operaciones
python -m unittest discover -s tests -t .       # pruebas automáticas
```
En Windows, si `python` no funciona, use `py main.py`.

## Estructura
- `main.py`: punto de entrada.
- `src/excepciones/`: jerarquía de excepciones personalizadas.
- `src/utilidades/`: logger y validadores reutilizables.
- `src/modelos/`: EntidadBase (abstracta), Cliente, Servicio (abstracta), ReservaSala, AlquilerEquipo, AsesoriaEspecializada y Reserva.
- `src/gestion/`: GestorFJ (listas internas y manejo seguro de errores).
- `simulacion/`: las 12 operaciones de demostración.
- `logs/eventos.log`: registro generado en cada ejecución.
- `docs/`: diagrama de clases e informe final en PDF.

## Conceptos aplicados
Abstracción (clases abstractas), herencia, polimorfismo (`_costo_base`, `validar_parametros`, `describir`),
encapsulación (atributos privados y propiedades), sobrecarga simulada (`calcular_costo` con parámetros opcionales),
excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.