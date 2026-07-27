# Interfaz grafica de la aplicacion, construida con Tkinter.
#
# Este modulo no sabe nada de TensorFlow ni de como se hace la prediccion:
# solo le pide los datos al usuario y muestra lo que le devuelve el
# ClasificadorIris. Por eso se podria cambiar por una web sin tocar model.py

import tkinter as tk
from tkinter import ttk

from app import flor
from app.model import ClasificadorIris

# Etiqueta de cada campo y un valor de ejemplo (fila 1 del dataset Iris).
# El ORDEN es obligatorio: es el mismo con el que se entreno el modelo.
CAMPOS = [
    ("Largo del sépalo (cm)", "5.1"),
    ("Ancho del sépalo (cm)", "3.5"),
    ("Largo del pétalo (cm)", "1.4"),
    ("Ancho del pétalo (cm)", "0.2"),
]

# Rango aceptable para una medida en centimetros. Sirve para atrapar errores
# de digitacion (por ejemplo escribir 51 en vez de 5.1).
MEDIDA_MINIMA = 0.0
MEDIDA_MAXIMA = 30.0


class VentanaPrincipal(tk.Tk):
    """Ventana principal del clasificador de flores Iris."""

    def __init__(self):
        super().__init__()

        self.title("Clasificador Iris - Modelo Neuronal")
        self.resizable(False, False)

        self._clasificador = None
        self._entradas = []

        self._construir_interfaz()

        # El modelo se carga DESPUES de mostrar la ventana. Si se cargara
        # antes, la app se veria congelada durante un segundo al arrancar.
        self.after(100, self._cargar_modelo)

    # ------------------------------------------------------------------
    # Construccion de la interfaz
    # ------------------------------------------------------------------

    def _construir_interfaz(self):
        marco = ttk.Frame(self, padding=20)
        marco.grid(row=0, column=0)

        ttk.Label(
            marco, text="CLASIFICADOR IRIS", font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 2))

        ttk.Label(
            marco,
            text="Red neuronal entrenada sobre el dataset Iris",
            font=("Segoe UI", 9),
            foreground="gray35",
        ).grid(row=1, column=0, columnspan=2, pady=(0, 16))

        # Columna izquierda: formulario y resultado
        panel_datos = ttk.Frame(marco)
        panel_datos.grid(row=2, column=0, sticky="n", padx=(0, 24))
        self._construir_formulario(panel_datos)

        # Columna derecha: dibujo de la flor
        panel_dibujo = ttk.Frame(marco)
        panel_dibujo.grid(row=2, column=1, sticky="n")
        self._construir_dibujo(panel_dibujo)

    def _construir_formulario(self, contenedor):
        for indice, (etiqueta, ejemplo) in enumerate(CAMPOS):
            ttk.Label(contenedor, text=etiqueta).grid(
                row=indice, column=0, sticky="w", pady=4, padx=(0, 10)
            )

            entrada = ttk.Entry(contenedor, width=12, justify="center")
            entrada.insert(0, ejemplo)
            entrada.grid(row=indice, column=1, pady=4)
            entrada.bind("<Return>", lambda evento: self._clasificar())

            self._entradas.append(entrada)

        self._boton = ttk.Button(
            contenedor, text="CLASIFICAR", command=self._clasificar, state="disabled"
        )
        self._boton.grid(row=4, column=0, columnspan=2, pady=(18, 6), sticky="ew")

        ttk.Separator(contenedor, orient="horizontal").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=8
        )

        self._resultado = ttk.Label(
            contenedor,
            text="Cargando modelo...",
            font=("Segoe UI", 12, "bold"),
            anchor="center",
        )
        self._resultado.grid(row=6, column=0, columnspan=2, pady=(4, 2))

        self._detalle = ttk.Label(
            contenedor,
            text="",
            font=("Consolas", 9),
            foreground="gray35",
            anchor="center",
            justify="center",
        )
        self._detalle.grid(row=7, column=0, columnspan=2, pady=(0, 4))

    def _construir_dibujo(self, contenedor):
        self._lienzo = tk.Canvas(
            contenedor,
            width=flor.LADO_LIENZO,
            height=flor.LADO_LIENZO,
            background="white",
            highlightthickness=1,
            highlightbackground="#d0d0d0",
        )
        self._lienzo.grid(row=0, column=0)

        ttk.Label(
            contenedor,
            text="Dibujo a escala real de las medidas ingresadas",
            font=("Segoe UI", 8),
            foreground="gray45",
        ).grid(row=1, column=0, pady=(6, 0))

        # Dibujo inicial en gris, con los valores de ejemplo
        flor.dibujar(self._lienzo, [float(ejemplo) for _, ejemplo in CAMPOS])

    # ------------------------------------------------------------------
    # Carga del modelo
    # ------------------------------------------------------------------

    def _cargar_modelo(self):
        try:
            self._clasificador = ClasificadorIris()
        except FileNotFoundError as error:
            self._resultado.config(text="Error al cargar el modelo", foreground="red")
            self._detalle.config(text=str(error))
            return

        self._boton.config(state="normal")
        self._resultado.config(text="Listo para clasificar", foreground="gray35")
        self._detalle.config(text="Ingresa las medidas y presiona CLASIFICAR")

    # ------------------------------------------------------------------
    # Logica de los eventos
    # ------------------------------------------------------------------

    def _clasificar(self):
        if self._clasificador is None:
            return

        try:
            medidas = self._leer_medidas()
        except ValueError as error:
            self._resultado.config(text="Dato inválido", foreground="red")
            self._detalle.config(text=str(error))
            flor.limpiar(self._lienzo)
            return

        especie, confianza, desglose = self._clasificador.predecir_detallado(medidas)

        self._resultado.config(
            text=f"{especie}  ({confianza * 100:.1f}%)", foreground="#1a6b1a"
        )

        self._detalle.config(
            text="\n".join(
                f"{nombre:<18} {probabilidad * 100:5.1f}%"
                for nombre, probabilidad in desglose.items()
            )
        )

        # La flor se repinta con el color de la especie predicha
        flor.dibujar(self._lienzo, medidas, especie)

    def _leer_medidas(self):
        """Lee los 4 campos y los valida. Lanza ValueError si algo esta mal."""
        medidas = []

        for entrada, (etiqueta, _) in zip(self._entradas, CAMPOS):
            texto = entrada.get().strip().replace(",", ".")

            if not texto:
                raise ValueError(f"Falta el campo: {etiqueta}")

            try:
                valor = float(texto)
            except ValueError:
                raise ValueError(f"'{texto}' no es un número válido en {etiqueta}")

            if not (MEDIDA_MINIMA < valor <= MEDIDA_MAXIMA):
                raise ValueError(
                    f"{etiqueta}: {valor} está fuera del rango esperado "
                    f"({MEDIDA_MINIMA}-{MEDIDA_MAXIMA} cm)"
                )

            medidas.append(valor)

        return medidas
