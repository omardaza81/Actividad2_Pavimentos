# Actividad 2 — Evaluación de la segmentación de fisuras en pavimentos

**Asignatura:** Percepción Computacional — Especialización en Inteligencia Artificial, UNIR
**Autor:** Omar Javier Daza Leguizamón
**Docente:** Luis Fernando Barajas Ardila
**Fecha:** 18 de octubre de 2026

Este trabajo compara tres segmentadores clásicos de fisuras en imágenes de pavimento: umbral de Otsu, crecimiento de regiones a partir de semillas (implementación propia) y Watershed controlada por marcadores. Los resultados se evalúan con un evaluador propio en NumPy, frente al *ground truth* de dos conjuntos públicos: CrackForest y DeepCrack. El análisis está en el informe; el código y sus resultados, en el notebook.

## Contenido de la entrega

| Archivo o carpeta | Descripción |
|---|---|
| `Informe_Actividad2_Percepcion_Computacional.pdf` | Memoria: teoría, metodología, resultados y análisis. Cita las celdas del notebook como (Notebook, celda [n]). |
| `Actividad2_Pavimentos.ipynb` | Notebook con el código y las salidas de la última ejecución completa. |
| `preparar_act2.py` | Comprueba el entorno y descarga los dos conjuntos de datos si no están presentes. |
| `requirements.txt` | Librerías de Python necesarias. |
| `resultados_act2/` | Figuras y tablas generadas por el notebook, incluidos los archivos de caché de la calibración y la evaluación. |
| `README.md` | Este archivo. |

Los conjuntos de datos **no se incluyen**, por tamaño (unos 130 MB) y por sus licencias. `preparar_act2.py` los descarga de sus repositorios oficiales.

## Requisitos

- Python 3.10 o superior (probado con Python 3.14).
- Unos 300 MB libres en disco y conexión a internet para la primera descarga de datos.
- Jupyter (Notebook, JupyterLab o VS Code con la extensión de Jupyter).

## Instalación y ejecución

Todos los archivos deben estar en la **misma carpeta**. Desde esa carpeta:

**1. Crear y activar un entorno virtual (recomendado)**

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

**2. Instalar las librerías**

```bash
pip install -r requirements.txt
```

**3. Preparar los datos**

```bash
python preparar_act2.py
```

El script comprueba las librerías, descarga y descomprime CrackForest en `data/` y DeepCrack en `data_deepcrack/`, y crea `resultados_act2/`. Se puede ejecutar varias veces sin riesgo: lo que ya existe no se descarga de nuevo. Debe terminar con `Todo listo para la Actividad 2.`

**4. Ejecutar el notebook**

Abra `Actividad2_Pavimentos.ipynb`, seleccione el kernel del entorno virtual y ejecute **Kernel → Restart & Run All**. Las celdas de código quedan numeradas de [1] a [25], la numeración que cita el informe.

## Tiempo de ejecución

| Situación | Tiempo aproximado |
|---|---|
| Con los archivos de caché de `resultados_act2/` (entrega por defecto) | 1 minuto |
| Sin caché: calibración (198 combinaciones) y evaluación (332 imágenes × 3 métodos) completas | 5 a 6 minutos |

Para repetir los cálculos aunque exista la caché, ponga `RECALIBRAR = True` (celda [17]) o `REEVALUAR = True` (celda [19]). También puede borrar `calibracion_rejilla.csv` y `resultados_evaluacion.csv`. Los resultados se recalculan de forma determinista: en una ejecución desde cero, en un entorno limpio, se obtuvieron valores idénticos a los entregados.

## Estructura de carpetas tras la preparación

```
carpeta_de_trabajo/
├── Actividad2_Pavimentos.ipynb
├── preparar_act2.py
├── requirements.txt
├── README.md
├── data/                 # CrackForest: image/, groundTruth/, seg/ (lo crea preparar_act2.py)
├── data_deepcrack/       # DeepCrack: train_img/, train_lab/, test_img/, test_lab/ (lo crea preparar_act2.py)
└── resultados_act2/      # figuras fig00–fig09 y tablas CSV
```

## Archivos que genera el notebook

| Archivo | Celda | Contenido |
|---|---|---|
| `control_calidad_ground_truth.csv`, `fig00_control_calidad.png` | [3] | Control de calidad del *ground truth* e imágenes excluidas |
| `particion_datos.csv` | [4] | Imágenes de calibración y de evaluación |
| `fig01_ejemplos_conjuntos.png` | [5] | Ejemplos de cada conjunto |
| `caracterizacion_ground_truth.csv`, `fig02_ancho_fisuras.png` | [6] | Proporción y ancho de fisura por imagen |
| `tabla_sensibilidad_metricas.csv` | [11] | Respuesta de las métricas a perturbaciones del *ground truth* |
| `fig03_prueba_visualizador.png` | [12] | Mapa de errores de prueba |
| `fig04_preprocesado.png` a `fig07_watershed_pasos.png` | [13]–[16] | Preprocesado y pasos intermedios de los tres segmentadores |
| `calibracion_rejilla.csv`, `parametros_seleccionados.csv` | [17]–[18] | Calibración de parámetros |
| `resultados_evaluacion.csv`, `tabla_resumen_evaluacion.csv` | [19]–[20] | Métricas por imagen y resumen |
| `fig08_diagramas_caja.png` | [21] | Distribución de las métricas |
| `tabla_wilcoxon.csv` | [22] | Prueba de Wilcoxon con ajuste de Holm |
| `tabla_generalizacion.csv` | [23] | Calibración frente a evaluación |
| `fig09_casos_CrackForest.png`, `fig09_casos_DeepCrack.png` | [24] | Casos representativos |

## Probar los segmentadores con otra imagen

La celda [25] aplica los tres segmentadores calibrados a una imagen a elección:

- **Opción A, una imagen de los conjuntos:** modifique `CONJUNTO_ELEGIDO` e `IMAGEN_ELEGIDA` (por ejemplo, `"049"` o `"11125-1"`). Se calculan las métricas porque la imagen tiene *ground truth*.
- **Opción B, una imagen propia:** indique su ruta en `RUTA_IMAGEN_PROPIA`, y opcionalmente una máscara en `RUTA_GT_PROPIA`. Elija `PERFIL_PARAMETROS = "CrackForest"` para fisuras finas o `"DeepCrack"` para fisuras anchas.

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `AssertionError: No se encuentra data/groundTruth` o `data_deepcrack` | Ejecute `python preparar_act2.py` desde la carpeta del notebook. |
| `[ERROR] Descarga fallida` en `preparar_act2.py` | Descargue el ZIP a mano desde la URL que indica el mensaje, guárdelo con el nombre indicado y vuelva a ejecutar el script. |
| `ModuleNotFoundError` en el notebook | El kernel no es el del entorno virtual. Seleccione el kernel de `.venv`, o ejecute `pip install -r requirements.txt` en el entorno que use Jupyter. |
| `NameError` en una celda | Las celdas se ejecutaron fuera de orden. Use **Restart & Run All**. |

## Datos y licencias

Ambos conjuntos se distribuyen para uso académico y de investigación no comercial, y se emplean aquí en ese marco.

- **CrackForest (CFD):** 118 imágenes de 480 × 320 px con *ground truth*. Repositorio: https://github.com/cuilimeng/CrackForest-dataset
  Shi, Y., Cui, L., Qi, Z., Meng, F. y Chen, Z. (2016). Automatic road crack detection using random structured forests. *IEEE Transactions on Intelligent Transportation Systems, 17*(12), 3434–3445.
- **DeepCrack:** 537 imágenes de 544 × 384 px (300 de *train* y 237 de *test*). Repositorio: https://github.com/yhlleo/DeepCrack
  Liu, Y., Yao, J., Lu, X., Xie, R. y Li, L. (2019). DeepCrack: A deep hierarchical feature learning architecture for crack segmentation. *Neurocomputing, 338*, 139–153.
