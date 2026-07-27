# se carga el modelo entrenado y las predicciones de especies
#
# Este modulo NO conoce la interfaz grafica. Recibe numeros y devuelve un
# resultado, por eso se podria cambiar Tkinter por una web sin tocar nada aca.

import json
from pathlib import Path

import numpy as np
from tensorflow import keras

# las rutas se calculan desde la ubicacion de este archivo, no desde donde se
# ejecute el programa asi mismo la app funciona sin importar el directorio en el que este

RAIZ = Path(__file__).resolve().parent.parent
RUTA_MODELO = RAIZ / "models" / "modelo_iris.h5"
RUTA_SCALER = RAIZ / "models" / "scaler.json"

# cantidad de medidas que espera el modelo (los 4 atributos de la flor)
NUMERO_DE_CARACTERISTICAS = 4


class ClasificadorIris:
    # Envuelve todo el modelo entrenado junto con su procesamiento

    def __init__(self, ruta_modelo=RUTA_MODELO, ruta_scaler=RUTA_SCALER):
        if not ruta_modelo.exists():
            raise FileNotFoundError(f"No se encontro el modelo en: {ruta_modelo}")
        if not ruta_scaler.exists():
            raise FileNotFoundError(f"No se encontro el scaler en: {ruta_scaler}")

        self._modelo = keras.models.load_model(ruta_modelo)

        with open(ruta_scaler, encoding="utf-8") as archivo:
            config = json.load(archivo)

        # El archivo .h5 guarda los pesos pero NO guarda la normalizacion ni
        # los nombres de las clases. Por eso se cargan aparte desde el JSON.
        self._media = np.array(config["mean"], dtype=np.float32)
        self._escala = np.array(config["scale"], dtype=np.float32)
        self._clases = config["classes"]
        self._nombres_caracteristicas = config["feature_names"]

    @property
    def clases(self):
        # Nombres de las especies que el modelo puede predecir
        return list(self._clases)

    def predecir(self, medidas):
        """
        Clasifica una flor a partir de sus cuatro medidas en centimetros.

        medidas: [largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo]
        retorna: (nombre_especie, confianza) con la confianza entre 0.0 y 1.0
        """
        if len(medidas) != NUMERO_DE_CARACTERISTICAS:
            raise ValueError(
                f"Se esperaban {NUMERO_DE_CARACTERISTICAS} medidas, "
                f"llegaron {len(medidas)}"
            )

        # Keras siempre espera un lote de muestras: la forma (1, 4) significa
        # "una sola flor con cuatro caracteristicas"
        entrada = np.array(medidas, dtype=np.float32).reshape(1, NUMERO_DE_CARACTERISTICAS)

        # ESTA es la linea que hace que la app acierte: el modelo fue entrenado
        # con datos normalizados, asi que hay que aplicarle la misma escala.
        entrada_normalizada = (entrada - self._media) / self._escala

        probabilidades = self._modelo.predict(entrada_normalizada, verbose=0)[0]
        indice = int(np.argmax(probabilidades))

        return self._clases[indice], float(probabilidades[indice])

    def predecir_detallado(self, medidas):
        """
        Igual que predecir(), pero ademas devuelve la probabilidad de cada
        especie. Util para mostrarle al usuario que tan seguro esta el modelo.

        retorna: (nombre_especie, confianza, {especie: probabilidad, ...})
        """
        entrada = np.array(medidas, dtype=np.float32).reshape(1, NUMERO_DE_CARACTERISTICAS)
        entrada_normalizada = (entrada - self._media) / self._escala

        probabilidades = self._modelo.predict(entrada_normalizada, verbose=0)[0]
        indice = int(np.argmax(probabilidades))

        desglose = {
            nombre: float(valor)
            for nombre, valor in zip(self._clases, probabilidades)
        }
        return self._clases[indice], float(probabilidades[indice]), desglose
