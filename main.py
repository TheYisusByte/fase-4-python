# -*- coding: utf-8 -*-
# Archivo: main.py
# Punto de entrada de Software FJ. Ejecutar desde la carpeta raíz del proyecto:
#   python main.py          (en Windows, si no funciona: py main.py)

from simulacion.operaciones import ejecutar_simulacion
from src.gestion import GestorFJ
from src.utilidades.logger import ARCHIVO_LOG


def main():
    """Crea el gestor, ejecuta la simulación e indica dónde quedó el registro."""
    gestor = GestorFJ()
    ejecutar_simulacion(gestor)
    print(f"\nRegistro de eventos y errores en: {ARCHIVO_LOG}")


# Esta condición evita que main() se ejecute si otro archivo importa main.py.
if __name__ == "__main__":
    main()