# Clasificador Iris — App de escritorio

Aplicación local en Python que clasifica una flor Iris a partir de sus cuatro
medidas, usando la red neuronal entrenada en la Actividad 1.

**Curso:** Implementación de Soluciones de Inteligencia Artificial
**SENA — Regional Tolima · Centro de Industria y Construcción · 2026**
**Aprendiz:** Juan Sebastián Martín Moncada

---

## Qué hace

Recibe las cuatro medidas de una flor (largo y ancho de sépalo y pétalo) y
predice a cuál de las tres especies pertenece, mostrando además la probabilidad
que el modelo asigna a cada una.

```
┌────────────────────────────────────────┐
│           CLASIFICADOR IRIS            │
│  Red neuronal entrenada sobre Iris     │
│                                        │
│  Largo del sépalo (cm)      [  5.1  ]  │
│  Ancho del sépalo (cm)      [  3.5  ]  │
│  Largo del pétalo (cm)      [  1.4  ]  │
│  Ancho del pétalo (cm)      [  0.2  ]  │
│                                        │
│  ┌──────────── CLASIFICAR ──────────┐  │
│  └──────────────────────────────────┘  │
│  ────────────────────────────────────  │
│        Iris-setosa   (99.9%)           │
│                                        │
│     Iris-setosa        99.9%           │
│     Iris-versicolor     0.0%           │
│     Iris-virginica      0.1%           │
└────────────────────────────────────────┘
```

---

## Requisitos

- **Python 3.10 o superior** ([descargar](https://www.python.org/downloads/)) —
  marcar *"Add Python to PATH"* durante la instalación.
- **Tkinter**, que viene incluido con Python. Para verificarlo:

  ```bash
  python -c "import tkinter; print(tkinter.TkVersion)"
  ```

---

## Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/martin15006/implementaciones-de-soluciones-con-inteligencia-artificial.git
cd implementaciones-de-soluciones-con-inteligencia-artificial/actividad-2-iris-app
```

**2. Crear el entorno virtual**

```bash
python -m venv venv
```

**3. Activarlo**

En Windows (PowerShell):

```bash
.\venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
source venv/bin/activate
```

Debe aparecer `(venv)` al inicio de la línea de la terminal.

**4. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

> Descarga aproximadamente 600 MB (TensorFlow). Puede tardar varios minutos.

---

## Uso

Con el entorno virtual activo y desde la carpeta `actividad-2-iris-app`:

```bash
python main.py
```

La ventana muestra *"Cargando modelo..."* durante un segundo y luego habilita el
botón. Se puede clasificar con el botón o presionando **Enter** en cualquier campo.

---

## Estructura del proyecto

```
actividad-2-iris-app/
├── app/
│   ├── __init__.py       Convierte la carpeta en un paquete de Python
│   ├── model.py          Carga el modelo y hace las predicciones
│   └── ui.py             Interfaz gráfica con Tkinter
├── models/
│   ├── modelo_iris.h5    Red neuronal entrenada (Actividad 1)
│   └── scaler.json       Parámetros de normalización y nombres de clases
├── main.py               Punto de entrada
├── requirements.txt      Dependencias
└── README.md             Este archivo
```

### Decisión de arquitectura

El proyecto separa **lógica** de **presentación**:

- `model.py` no importa Tkinter. Recibe números y devuelve un resultado.
- `ui.py` no importa TensorFlow. Solo pide datos y muestra respuestas.

Gracias a esa separación, cambiar la interfaz de escritorio por una web (Flask,
Streamlit) o exponerla como API no requeriría modificar `model.py`. Es la
aplicación concreta de los principios de **baja dependencia y alta cohesión**.

---

## Resultados de las pruebas

Siete pruebas con valores reales del dataset Iris original:

| # | Medidas (cm) | Predicción | Especie real | ¿Correcto? | Confianza |
|---|---|---|---|---|---|
| 1 | 5.1 / 3.5 / 1.4 / 0.2 | Iris-setosa | Iris-setosa | ✅ Sí | 99.9% |
| 2 | 4.9 / 3.0 / 1.4 / 0.2 | Iris-setosa | Iris-setosa | ✅ Sí | 99.4% |
| 3 | 7.0 / 3.2 / 4.7 / 1.4 | Iris-versicolor | Iris-versicolor | ✅ Sí | 47.5% |
| 4 | 6.4 / 3.2 / 4.5 / 1.5 | Iris-virginica | Iris-versicolor | ❌ No | 46.6% |
| 5 | 6.3 / 3.3 / 6.0 / 2.5 | Iris-virginica | Iris-virginica | ✅ Sí | 96.8% |
| 6 | 5.8 / 2.7 / 5.1 / 1.9 | Iris-virginica | Iris-virginica | ✅ Sí | 68.7% |
| 7 | 5.5 / 2.6 / 4.4 / 1.2 | Iris-versicolor | Iris-versicolor | ✅ Sí | 86.4% |

**Precisión: 6 aciertos de 7 = 85.7%**

### Análisis

El único error (prueba 4) es una flor *versicolor* clasificada como *virginica*,
y el modelo lo reporta con apenas **46.6% de confianza** — es decir, el modelo
"sabe" que está dudando. Esa confusión coincide exactamente con la matriz de
confusión de la Actividad 1, donde los únicos errores también ocurrieron entre
esas dos especies. *Iris-setosa*, en cambio, se clasifica con más del 99% de
certeza, porque está completamente separada en el espacio de características.

El 85.7% de estas pruebas es consistente con el accuracy obtenido durante el
entrenamiento. Las diferencias entre ambas cifras se explican por el tamaño de
la muestra: 7 pruebas frente a 30 del conjunto de test. Con tan pocos casos,
un solo acierto o error mueve el porcentaje más de 14 puntos.

---

## Nota técnica: por qué existe `scaler.json`

Al inspeccionar el archivo `modelo_iris.h5` con `h5py` se comprobó que contiene
**solo** tres bloques: la arquitectura de la red, sus 193 pesos entrenados y el
estado del optimizador Adam. **No incluye el `StandardScaler`** que se usó para
normalizar los datos durante el entrenamiento.

Esto significa que una app que reciba centímetros crudos y se los pase
directamente al modelo obtiene predicciones incorrectas. Se verificó
experimentalmente con las mismas 7 pruebas:

| Versión | Aciertos | Comportamiento |
|---|---|---|
| **Con normalización** | **6/7 (85.7%)** | Confianzas realistas entre 47% y 99% |
| Sin normalizar | 2/7 (28.6%) | Predice *virginica* casi siempre, con 99–100% de "confianza" |

La versión sin normalizar **no lanza ningún error**: abre, responde y muestra
porcentajes altísimos. Simplemente se equivoca. Por eso los parámetros de
normalización se guardan en `scaler.json` y se aplican en `model.py` antes de
cada predicción:

```python
entrada_normalizada = (entrada - self._media) / self._escala
```

Se eligió **JSON en lugar de un `.pkl`** por cuatro razones: evita depender de
scikit-learn solo para hacer una resta y una división, no se rompe entre
versiones de librerías, es legible por un humano, y no representa un riesgo de
seguridad — cargar un pickle de origen desconocido puede ejecutar código
arbitrario.

---

## Licencia

Trabajo académico desarrollado para el SENA — Regional Tolima.
