# Implementaciones de Soluciones con Inteligencia Artificial

Repositorio de actividades del curso **IMPLEMENTACION DE SOLUCIONES DE INTELIGENCIA ARTIFICIAL**
SENA — Regional Tolima | Centro de Industria y Construcción | 2026

**Aprendiz:** Juan Sebastián Martín Moncada

---

## Contenido

| Actividad | Tema | Estado |
|---|---|---|
| [1 — Cuaderno de IA en Colab](./actividad-1-iris-colab/) | EDA + red neuronal sobre el dataset Iris | Completada |
| [2 — App con Python, GitHub y Claude AI](./actividad-2-iris-app/) | App de escritorio con Tkinter que consume el modelo |  En desarrollo |

---

## Actividad 1 — Mi Primer Cuaderno de IA

Análisis exploratorio (EDA) y entrenamiento de un clasificador sobre el dataset **Iris**
(150 muestras, 3 especies, 4 características morfológicas).

**Herramientas:** Google Colab · Gemini · pandas · matplotlib · seaborn · TensorFlow/Keras

### Arquitectura del modelo

```
Entrada (4 características)
   ↓
Dense(10, relu)      →  50 parámetros
   ↓
Dense(10, relu)      → 110 parámetros
   ↓
Dense(3, softmax)    →  33 parámetros
                     ─────────────────
              TOTAL  → 193 parámetros
```

- **División de datos:** 60% entrenamiento / 20% validación / 20% prueba
- **Preprocesamiento:** `StandardScaler` (media 0, desviación 1) + `LabelEncoder` + one-hot
- **Entrenamiento:** 50 épocas, `batch_size=8`, optimizador Adam (`lr=0.001`)
- **Salida:** `modelo_iris.h5` (formato HDF5, 34 KB)

### Resultados

> **Pendiente:** completar con los resultados de mi propia ejecución.
> Los pesos iniciales de la red no tienen semilla fija (`tf.random.set_seed()`),
> por lo que el accuracy varía en cada ejecución.

| Métrica | Valor |
|---|---|
| Accuracy en test | _(pendiente)_ |
| F1-score Iris-setosa | _(pendiente)_ |
| F1-score Iris-versicolor | _(pendiente)_ |
| F1-score Iris-virginica | _(pendiente)_ |

### Hallazgo técnico

Al inspeccionar el archivo `.h5` con `h5py` se confirmó que **contiene únicamente**
la arquitectura, los 193 pesos entrenados y el estado del optimizador Adam —
**no incluye el `StandardScaler`**. Esto implica que cualquier aplicación que
consuma el modelo debe normalizar las entradas por su cuenta antes de predecir,
o las predicciones serán incorrectas.

---

## Actividad 2 — App de escritorio con Tkinter

Aplicación local que carga el modelo de la Actividad 1 y clasifica una flor
a partir de sus cuatro medidas.

 Instrucciones de instalación y uso: [`actividad-2-iris-app/README.md`](./actividad-2-iris-app/)

---

## Licencia y uso

Trabajo académico. El material de apoyo del curso (PDFs del instructor) no se
publica en este repositorio.
