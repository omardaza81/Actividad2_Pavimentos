# Eliminación de ruido impulsivo en imágenes de pavimento preservando fisuras

**Laboratorio:** Eliminación de anomalías de la imagen
**Asignatura:** Percepción Computacional, Especialización en Inteligencia Artificial, UNIR Colombia
**Autor:** Omar Javier Daza Leguizamón
**Fecha:** octubre de 2026

## Descripción

El notebook implementa un método propio para eliminar ruido impulsivo ("sal y pimienta") en
imágenes de pavimento, conservando las fisuras, que son el dato de interés para la auscultación.
El método trabaja en dos etapas:

1. **Detección:** un píxel se marca como impulso si tiene valor extremo (0 o 255) y está aislado,
   es decir, tiene a lo sumo K vecinos similares en su vecindario 3 × 3.
2. **Corrección:** cada impulso se reemplaza por la mediana de sus vecinos limpios, con una ventana
   que crece de 3 × 3 hasta 7 × 7 solo cuando no hay suficientes vecinos limpios.

Ambas etapas se aplican en dos pasadas. Parámetros: K = 3, T = 30, N = 5, V_max = 7, P = 2,
idénticos para todas las imágenes y densidades. El método se compara con el filtro de mediana
3 × 3 y 5 × 5 mediante PSNR global, PSNR en la zona de fisura y SSIM.

## Contenido de la entrega

```
Actividad1_Pavimentos/
├── README.md                        ← este archivo
├── Actividad1_Pavimentos.ipynb      ← notebook con la solución
├── Actividad1_Pavimentos.pdf        ← ejecución completa del notebook
├── requirements.txt                 ← librerías necesarias
└── data/                            ← datos (subconjunto de CrackForest)
    ├── README.md                    ← README original del conjunto (licencia y cita)
    ├── image/
    │   ├── 035.jpg
    │   ├── 049.jpg
    │   ├── 096.jpg
    │   └── 097.jpg
    └── groundTruth/
        ├── 035.mat
        ├── 049.mat
        ├── 096.mat
        └── 097.mat
```

## Requisitos

- Python 3.10 o superior. El notebook se ejecutó y verificó con Python 3.14.6 en Windows 11.
- Librerías: NumPy, OpenCV, Matplotlib, SciPy (solo para leer las máscaras `.mat`) e ipykernel,
  listadas en `requirements.txt`.
- No requiere conexión a internet: los datos se incluyen en la carpeta `data/`.

## Instalación

Desde la carpeta `Actividad1_Pavimentos`, crear y activar un entorno virtual, e instalar las
librerías:

**Windows (PowerShell)**

```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS / Linux**

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

1. Abrir `Actividad1_Pavimentos.ipynb` en Jupyter o en Visual Studio Code y seleccionar como
   kernel el entorno virtual creado.
2. Reiniciar el kernel y ejecutar todas las celdas en orden (Reiniciar → Ejecutar todo).
3. La ejecución completa tarda aproximadamente entre 1 y 2 minutos, según el equipo.

El notebook usa rutas relativas (`data/...`), por lo que debe ejecutarse con la carpeta de
trabajo en `Actividad1_Pavimentos`, sin mover el notebook fuera de ella.

## Reproducibilidad

El ruido se genera con una semilla aleatoria fija (`SEMILLA = 2026`), de modo que cada ejecución
produce exactamente los mismos resultados. Promedios esperados de las cuatro imágenes
(PSNR global en dB / PSNR en fisura en dB / SSIM):

| Densidad de ruido | Mediana 3 × 3          | Mediana 5 × 5          | Método propuesto       |
|-------------------|------------------------|------------------------|------------------------|
| 5 %               | 28,36 / 24,75 / 0,675  | 26,09 / 21,46 / 0,423  | 40,20 / 36,25 / 0,985  |
| 15 %              | 27,45 / 24,09 / 0,649  | 25,99 / 21,36 / 0,420  | 35,25 / 31,43 / 0,952  |
| 30 %              | 22,82 / 20,60 / 0,516  | 25,70 / 20,97 / 0,411  | 31,20 / 27,45 / 0,885  |

## Datos

Las imágenes y máscaras provienen del conjunto **CrackForest**:

- Repositorio: https://github.com/cuilimeng/CrackForest-dataset
- Cita: Shi, Y., Cui, L., Qi, Z., Meng, F. y Chen, Z. (2016). Automatic road crack detection
  using random structured forests. *IEEE Transactions on Intelligent Transportation Systems*,
  17(12), 3434–3445.
- Licencia: uso no comercial con fines de investigación, según el README original incluido en
  `data/README.md`.

Se incluyen únicamente las cuatro imágenes analizadas y sus máscaras. Cada máscara (`.mat`)
contiene la matriz `Segmentation`, donde 1 corresponde a pavimento y 2 a fisura.

## Notas técnicas

- Las métricas PSNR y SSIM se implementaron en el propio notebook según sus definiciones
  originales (SSIM: Wang et al., 2004), sin depender de scikit-image, para reducir las
  dependencias del proyecto.
- El uso de herramientas de inteligencia artificial durante el desarrollo se declara en la
  sección correspondiente del notebook.
