# Preguntas de reflexión — Actividad 1

**Aprendiz:** Juan Sebastián Martín Moncada
**Curso:** Implementación de Soluciones de Inteligencia Artificial — SENA Regional Tolima

Resultados obtenidos en mi ejecución (30 muestras de prueba):

| Especie | Precision | Recall | F1-score | Muestras |
|---|---|---|---|---|
| Iris-setosa | 1.00 | 1.00 | 1.00 | 10 |
| Iris-versicolor | 0.90 | 0.90 | 0.90 | 10 |
| Iris-virginica | 0.90 | 0.90 | 0.90 | 10 |
| **Accuracy** | | | **0.93** | **30** |

---

## 1. ¿Cuál especie fue la más fácil de clasificar? ¿Por qué?

**Iris-setosa**, sin discusión: 10 aciertos de 10, con precision, recall y F1-score de 1.00. Ni un solo error.

La razón no está en la matriz de confusión sino en el EDA. En el pair plot, el grupo de *setosa* aparece completamente aislado de los otros dos: su `PetalLengthCm` ronda 1 a 2 cm, mientras *versicolor* y *virginica* van de 3 a 6.9 cm, **sin ningún solapamiento**. Es decir, basta con mirar el largo del pétalo para identificarla — es linealmente separable.

Los 2 errores de mi modelo (accuracy 0.93 = 28 de 30) ocurrieron entre *versicolor* y *virginica*, que son justamente las dos especies cuyas nubes de puntos se superponen en la frontera. Mi matriz de confusión quedó así:

```
                  predicho →
                setosa  versicolor  virginica
real  setosa       10        0          0
      versicolor    0        9          1
      virginica     0        1          9
```

---

## 2. ¿Qué diferencia hay entre las distribuciones de sépalo y de pétalo?

Hay dos diferencias, y ambas se ven en los histogramas y en el `describe()`:

**Forma.** Las variables de sépalo tienen una distribución **unimodal**, aproximadamente normal — un solo pico. Las de pétalo son claramente **bimodales**: dos picos separados, uno pequeño alrededor de 1–2 cm y otro más amplio entre 3 y 7 cm.

**Dispersión.** Los datos del dataset completo:

| Variable | Rango | Desviación estándar |
|---|---|---|
| SepalLengthCm | 4.3 – 7.9 | 0.83 |
| SepalWidthCm | 2.0 – 4.4 | **0.44** |
| PetalLengthCm | 1.0 – 6.9 | **1.77** |
| PetalWidthCm | 0.1 – 2.5 | 0.76 |

El largo del pétalo se dispersa **cuatro veces más** que el ancho del sépalo.

**Por qué importa:** la bimodalidad significa que los grupos ya vienen separados en los datos crudos, sin que el modelo haga nada. Por eso el pétalo es discriminativo y el sépalo no. Los box plots lo confirman: las cajas de pétalo por especie casi no se tocan, mientras que las de sépalo se solapan bastante.

---

## 3. ¿Qué pasaría si entrenáramos el modelo solo con las variables de pétalo?

En general **no empeoraría**, y podría incluso mejorar ligeramente. La razón es que el pétalo concentra casi toda la capacidad discriminativa, mientras que el sépalo aporta más ruido que señal. Además, con menos variables de entrada el modelo tiene menos parámetros, lo que ayuda cuando el conjunto de entrenamiento es pequeño (apenas 90 muestras).

**Pero hay que ser honesto con la estadística:** el conjunto de prueba tiene solo 30 muestras, así que una sola flor mueve el accuracy 3.3 puntos. Una diferencia de 0.93 a 0.96 **no demuestra nada por sí sola** — podría ser puro azar de la inicialización de los pesos, que en este cuaderno no tiene semilla fija (`tf.random.set_seed()` no está definido). Para afirmarlo con seriedad habría que repetir el experimento varias veces y comparar el rango de resultados, no un número suelto.

---

## 4. ¿Para qué sirve el archivo `.h5`? Menciona un caso de uso real

El `.h5` es un contenedor binario en formato **HDF5** (*Hierarchical Data Format v5*) que guarda el modelo ya entrenado, para no tener que volver a entrenarlo. Al inspeccionarlo con la librería `h5py` comprobé que contiene tres bloques:

- `model_config` — la arquitectura de la red, en formato JSON
- `model_weights` — los **193 pesos** entrenados, repartidos en las 3 capas (50 + 110 + 33)
- `optimizer_weights` — el estado del optimizador Adam, que permite *reanudar* el entrenamiento

Entrenar es costoso; predecir es barato. El `.h5` separa las dos cosas: se carga con `tf.keras.models.load_model()` y queda listo para clasificar en milisegundos, en otro computador y en otro momento.

**Caso de uso real:** exactamente lo que construí en la Actividad 2 — una aplicación de escritorio donde el usuario escribe las cuatro medidas de una flor y obtiene la especie al instante, sin conexión a internet y sin entrenar nada. El mismo principio se usa para publicar un modelo detrás de una API (Flask, FastAPI) o dentro de una app móvil.

**Una limitación importante que descubrí:** el `.h5` guarda **únicamente la red neuronal**. No incluye el `StandardScaler` ni el `LabelEncoder`. Si se carga el modelo en otro entorno y se le pasan medidas en centímetros sin normalizar, las predicciones salen incorrectas **sin lanzar ningún error**. Lo comprobé experimentalmente en la Actividad 2: con normalización acerté 6 de 7 pruebas; sin normalizar, solo 2 de 7 — y en ese caso el modelo reportaba 99% de confianza estando equivocado. Por eso, para un despliegue real hay que guardar también esos objetos, y el modelo y su preprocesamiento deben tratarse como un par inseparable.

*(Nota adicional: Keras advierte que `.h5` es un formato legacy y recomienda el nativo `.keras`.)*
