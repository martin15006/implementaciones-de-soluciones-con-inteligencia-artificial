# Punto de entrada de la aplicacion.
#
# Este archivo no contiene logica: solo arranca la ventana. Mantenerlo asi de
# corto hace evidente donde empieza el programa.

from app.ui import VentanaPrincipal


def main():
    ventana = VentanaPrincipal()
    ventana.mainloop()


# Solo se ejecuta si el archivo se corre directamente (python main.py),
# no si alguien lo importa desde otro modulo.
if __name__ == "__main__":
    main()
