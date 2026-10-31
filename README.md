Software FJ - Sistema Integral de Gestion de Clientes, Servicios y Reservas

Trabajo colaborativo de Programacion (UNAD, Ingenieria de Sistemas) - Fase 4.
Sistema orientado a objetos en Python, **sin base de datos**: todo se maneja con
objetos y listas; solo se usa un archivo para guardar los logs.

## Como ejecutarlo
    python main.py

Solo necesita Python 3 (no se instalan librerias). El log queda en `logs/software_fj.log`.
## Conceptos aplicados
- **Abstraccion:** `Entidad` y `Servicio` son clases abstractas.
- **Herencia y polimorfismo:** los tres servicios sobrescriben `calcular_costo_base`, `validar_parametros` y `describir`.
- **Encapsulacion:** atributos privados en `Cliente` con `property` y validaciones.
- **Sobrecarga:** `calcular_costo(horas, descuento, impuesto)` con parametros opcionales (en Python se simula asi).
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/finally`, `try/except/else/finally` y encadenamiento con `raise ... from e`.

## Integrantes y modulos
| Integrante | Modulo |
|---|---|
| Integrante 1 | `excepciones.py`, `registro_logs.py` |
| Integrante 2 | `entidades.py`, `cliente.py` |
| Integrante 3 | `servicios.py` |
| Integrante 4 | `reserva.py` |
| Integrante 5 | `gestor.py`, `main.py` |
