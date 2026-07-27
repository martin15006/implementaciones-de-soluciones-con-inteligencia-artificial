# Preguntas de reflexión — Actividad 2

**Aprendiz:** Juan Sebastián Martín Moncada
**Curso:** Implementación de Soluciones de Inteligencia Artificial — SENA Regional Tolima

---

## 1. ¿Cuál fue el mayor reto técnico y cómo lo solucionaste?

El mayor reto no fue escribir la app, sino **descubrir un problema que no daba
ningún error**.

Antes de programar, inspeccioné el archivo `modelo_iris.h5` con la librería
`h5py` para entender qué contiene realmente. Encontré tres bloques: la
arquitectura de la red en formato JSON, los 193 pesos entrenados y el estado del
optimizador Adam. Y encontré también lo que **no** contenía: el `StandardScaler`
que se usó en la Actividad 1 para normalizar los datos antes de entrenar.

Eso significaba que si la app le pasaba las medidas en centímetros directamente
al modelo, las predicciones iban a estar mal — porque el modelo nunca vio
centímetros durante su entrenamiento, vio valores normalizados con media 0 y
desviación 1.

Lo grave es que este error **no produce ningún mensaje de fallo**. La app abre,
el botón responde, aparece un resultado con su porcentaje. Simplemente miente.
Lo comprobé ejecutando las mismas 7 pruebas de las dos formas:

| Versión | Aciertos | Comportamiento |
|---|---|---|
| Con normalización | 6/7 (85.7%) | Confianzas realistas de 47% a 99% |
| Sin normalizar | 2/7 (28.6%) | Predice *virginica* casi siempre, con 99–100% de "confianza" |

**La solución** fue volver al cuaderno de Colab y extraer los parámetros del
scaler (`mean_` y `scale_`), junto con el orden de las clases del
`LabelEncoder`. Los guardé en `models/scaler.json` y apliqué la normalización
en `model.py` antes de cada predicción:

```python
entrada_normalizada = (entrada - self._media) / self._escala
```

Un detalle que me pareció interesante: los parámetros del scaler **sí son
reproducibles**, aunque los pesos de la red no lo sean. Como `train_test_split`
usa `random_state=42` fijo, el conjunto de entrenamiento siempre es el mismo y
por lo tanto la media y la desviación siempre dan igual. Lo único aleatorio son
los pesos iniciales de la red, porque el cuaderno no define `tf.random.set_seed()`.

**Lo que me llevo:** el error que no se ve es más peligroso que el que revienta.
Un programa que falla te avisa; uno que se equivoca en silencio te deja
entregando resultados incorrectos sin enterarte.

---

## 2. ¿Qué ventajas tiene GitHub frente a guardar los archivos en una carpeta local?

**Historial real.** Git guarda cada versión con su fecha, su autor y su mensaje.
No hace falta el clásico `app_v1.py`, `app_v2.py`, `app_FINAL.py`,
`app_FINAL_de_verdad.py`. Si algo se rompe, se puede ver exactamente qué cambió
y volver atrás.

**Respaldo fuera del computador.** Si se daña el disco, el proyecto sigue
existiendo. Una carpeta local es un único punto de falla.

**Portabilidad.** Cualquier persona puede clonar el repositorio y ejecutar la app
en su máquina siguiendo el README. No hay que mandar carpetas comprimidas por
correo ni preguntar "¿cuál era la última versión?".

**Colaboración.** Varias personas pueden trabajar sobre el mismo proyecto sin
pisarse, cada una en su rama, y unir los cambios después.

**Es la evidencia del proceso.** Los commits muestran cómo se construyó el
proyecto paso a paso, no solo el resultado final.

Una lección concreta que aprendí durante esta actividad: **`.gitignore` solo
funciona sobre archivos que Git todavía no rastrea**. Si un archivo ya fue
subido, hay que sacarlo explícitamente con `git rm --cached`, porque ignorarlo
después no lo borra del historial. De ahí la regla de que en Git nunca se
commitea una contraseña o una API key pensando "después la borro" — el pasado
del repositorio no se borra tan fácil.

---

## 3. ¿Qué pasos debería seguir otra persona para ejecutar mi app?

1. **Instalar Python 3.10 o superior** desde python.org, marcando la casilla
   *"Add Python to PATH"* durante la instalación.

2. **Instalar Git** desde git-scm.com, si no lo tiene.

3. **Clonar el repositorio** y entrar a la carpeta del proyecto:

   ```bash
   git clone https://github.com/martin15006/implementaciones-de-soluciones-con-inteligencia-artificial.git
   cd implementaciones-de-soluciones-con-inteligencia-artificial/actividad-2-iris-app
   ```

4. **Crear un entorno virtual** para que las librerías del proyecto no se mezclen
   con las del resto de su computador:

   ```bash
   python -m venv venv
   ```

5. **Activarlo.** En Windows: `.\venv\Scripts\Activate.ps1`. En macOS o Linux:
   `source venv/bin/activate`. Debe aparecer `(venv)` al inicio de la línea.

6. **Instalar las dependencias** listadas en `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   Son unos 600 MB, casi todo TensorFlow. Tarda varios minutos.

7. **Ejecutar la aplicación:**

   ```bash
   python main.py
   ```

No necesita descargar el modelo por separado: tanto `modelo_iris.h5` como
`scaler.json` viajan dentro del repositorio, en la carpeta `models/`. Tampoco
necesita instalar Tkinter, porque viene incluido con Python.

---

## 4. ¿Qué pasaría si cambiara el `.h5` por uno entrenado con más datos? ¿Habría que modificar la app?

**Depende de qué cambie en el modelo nuevo, y hay una trampa.**

**Si el modelo nuevo conserva la misma forma** — 4 características de entrada y
las mismas 3 especies de salida — entonces `model.py` y `ui.py` **no necesitan
ni una línea de cambio**. Basta reemplazar el archivo en `models/`. Esa es
precisamente la ventaja de haber separado la lógica de la interfaz: el modelo es
un dato, no código.

**Pero hay que reemplazar también `scaler.json`.** Este es el punto que se pasa
por alto: si el modelo se entrena con más datos, el conjunto de entrenamiento
cambia, y por lo tanto **la media y la desviación estándar también cambian**. Si
se actualiza el `.h5` pero se deja el `scaler.json` viejo, la app vuelve a caer
en el mismo error silencioso del punto 1: normaliza con los números equivocados
y predice mal sin avisar. **El modelo y su scaler son un par inseparable.**

**Sí habría que modificar la app** en estos casos:

- **Si cambia el número de características.** Habría que agregar o quitar campos
  en `ui.py` y ajustar la constante `NUMERO_DE_CARACTERISTICAS` en `model.py`.
- **Si cambia el número de clases.** Por ejemplo, si el modelo aprendiera a
  reconocer una cuarta especie. En este caso la app se adapta casi sola, porque
  los nombres se leen desde `scaler.json`, pero habría que verificar el
  formato de la salida.
- **Si cambia el preprocesamiento.** Si en vez de `StandardScaler` se usara
  `MinMaxScaler`, la fórmula de normalización sería otra y habría que cambiarla
  en `model.py`.

En resumen: **más datos, misma estructura → solo se cambian los archivos de
`models/`** (los dos, no uno). **Estructura distinta → hay que tocar el código.**

---

## 5. ¿Qué es un *fork* en GitHub y para qué sirve?

Un **fork** es una copia completa de un repositorio ajeno dentro de tu propia
cuenta de GitHub. Es un repositorio independiente, con su propio historial, sobre
el que tienes permisos totales — pero GitHub recuerda de dónde salió.

**Para qué sirve:**

- **Contribuir a proyectos de otros.** No puedes escribir directamente en el
  repositorio de alguien más. El flujo estándar es: haces *fork*, clonas tu copia,
  haces los cambios en una rama, y abres un ***pull request*** proponiendo que el
  dueño original incorpore tu trabajo. Así funciona prácticamente todo el software
  libre.

- **Partir de un proyecto existente.** Si un proyecto te sirve como base pero
  quieres llevarlo por otro camino, el fork te da el punto de partida completo
  con todo su historial.

- **Experimentar sin riesgo.** Puedes romper lo que quieras en tu copia sin
  afectar el original.

**Diferencia con un `clone`:** clonar descarga el repositorio a tu computador,
pero sigue apuntando al repositorio original — si no tienes permisos, no puedes
subir nada. El fork crea una copia **en tu cuenta de GitHub**, a la que sí puedes
subir. En la práctica se usan juntos: primero haces el fork, después clonas tu
fork.

**Diferencia con una rama (`branch`):** una rama vive dentro del mismo
repositorio y es para organizar tu propio trabajo. Un fork es un repositorio
aparte, bajo otra cuenta, y es para trabajar sobre código de alguien más.
