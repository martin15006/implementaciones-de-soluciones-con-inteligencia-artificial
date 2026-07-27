# Dibujo de la flor sobre un Canvas de Tkinter.
#
# No es un adorno: los petalos y sepalos se dibujan con el tamano REAL que
# escribio el usuario, a una escala fija de pixeles por centimetro. Por eso
# una setosa se ve chiquita y una virginica se ve grande.
#
# Este modulo tampoco conoce el modelo: solo recibe medidas y un nombre de
# especie (para elegir el color) y dibuja.

import math

# Escala del dibujo. La medida mas grande del dataset es ~7.9 cm, asi que
# 7.9 * 15 = 118 px de radio, que cabe en un lienzo de 260 px.
PIXELES_POR_CM = 15
LADO_LIENZO = 260

# Los iris de verdad tienen 3 sepalos que caen y 3 petalos que apuntan arriba.
# En Tkinter el eje Y crece hacia abajo, asi que 90 grados apunta hacia abajo.
ANGULOS_SEPALOS = (90, 210, 330)
ANGULOS_PETALOS = (270, 30, 150)

COLORES = {
    "Iris-setosa": {"petalo": "#9b8cd4", "sepalo": "#6f5fa8"},
    "Iris-versicolor": {"petalo": "#5b93d6", "sepalo": "#376ba8"},
    "Iris-virginica": {"petalo": "#a85fc0", "sepalo": "#71318a"},
}
COLOR_SIN_PREDICCION = {"petalo": "#c9c9c9", "sepalo": "#a8a8a8"}
COLOR_CENTRO = "#f2c94c"


def _puntos_de_petalo(centro_x, centro_y, angulo_grados, largo_px, ancho_px, pasos=28):
    """
    Calcula los puntos de una elipse que nace en el centro de la flor y se
    extiende hacia el angulo indicado. Tkinter no sabe rotar elipses, asi que
    se construye como un poligono y se le pide que lo suavice.
    """
    angulo = math.radians(angulo_grados)
    coseno = math.cos(angulo)
    seno = math.sin(angulo)

    semi_largo = largo_px / 2
    semi_ancho = ancho_px / 2

    puntos = []
    for paso in range(pasos):
        t = 2 * math.pi * paso / pasos

        # Elipse en coordenadas locales: nace en (0, 0) y crece hacia +x
        x_local = semi_largo * math.cos(t) + semi_largo
        y_local = semi_ancho * math.sin(t)

        # Se rota el punto y se traslada al centro de la flor
        puntos.append(centro_x + x_local * coseno - y_local * seno)
        puntos.append(centro_y + x_local * seno + y_local * coseno)

    return puntos


def dibujar(lienzo, medidas, especie=None):
    """
    Dibuja la flor en el lienzo recibido.

    medidas: [largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo] en cm
    especie: nombre de la especie predicha, o None para dibujarla en gris
    """
    lienzo.delete("all")

    largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo = medidas
    colores = COLORES.get(especie, COLOR_SIN_PREDICCION)

    centro = LADO_LIENZO / 2

    # Los sepalos van primero para que queden por detras de los petalos
    for angulo in ANGULOS_SEPALOS:
        lienzo.create_polygon(
            _puntos_de_petalo(
                centro,
                centro,
                angulo,
                largo_sepalo * PIXELES_POR_CM,
                ancho_sepalo * PIXELES_POR_CM,
            ),
            fill=colores["sepalo"],
            outline="",
            smooth=True,
        )

    for angulo in ANGULOS_PETALOS:
        lienzo.create_polygon(
            _puntos_de_petalo(
                centro,
                centro,
                angulo,
                largo_petalo * PIXELES_POR_CM,
                ancho_petalo * PIXELES_POR_CM,
            ),
            fill=colores["petalo"],
            outline="",
            smooth=True,
        )

    radio_centro = 7
    lienzo.create_oval(
        centro - radio_centro,
        centro - radio_centro,
        centro + radio_centro,
        centro + radio_centro,
        fill=COLOR_CENTRO,
        outline="",
    )

    _dibujar_regla(lienzo)


def limpiar(lienzo):
    """Borra la flor y deja solo la regla de escala."""
    lienzo.delete("all")
    _dibujar_regla(lienzo)


def _dibujar_regla(lienzo):
    """Referencia de escala, para dejar claro que el dibujo esta a tamano real."""
    x = 12
    y = LADO_LIENZO - 14

    lienzo.create_line(x, y, x + PIXELES_POR_CM, y, fill="#8a8a8a", width=2)
    lienzo.create_line(x, y - 3, x, y + 3, fill="#8a8a8a", width=2)
    lienzo.create_line(
        x + PIXELES_POR_CM, y - 3, x + PIXELES_POR_CM, y + 3, fill="#8a8a8a", width=2
    )
    lienzo.create_text(
        x + PIXELES_POR_CM + 16,
        y,
        text="1 cm",
        fill="#6a6a6a",
        font=("Segoe UI", 8),
    )
