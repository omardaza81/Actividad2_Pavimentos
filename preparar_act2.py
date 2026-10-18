"""
preparar_act2.py — Configuración complementaria para la Actividad 2
(Percepción Computacional, UNIR): evaluación de segmentadores de fisuras.

Qué hace (se puede ejecutar varias veces sin riesgo):
  1. Revisa la versión de Python y qué librerías ya están instaladas en la .venv.
  2. Verifica CrackForest (CFD) en data/; si no está (p. ej., en el equipo del docente), lo descarga.
  3. Descarga y descomprime DeepCrack en data_deepcrack/ (solo si no existe).
  4. Crea la carpeta resultados_act2/ para figuras y tablas.

No modifica data/ si ya existe, ni el notebook, ni los demás archivos de la carpeta.

Uso (desde la carpeta del notebook, con el entorno virtual activado):
    python preparar_act2.py
"""

import sys
import importlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# Librerías que usará la Actividad 2: (nombre para importar, nombre en pip, uso)
NUCLEO = [
    ("numpy", "numpy", "matrices y métricas propias"),
    ("scipy", "scipy", "lectura de .mat (CFD) y transformada de distancia"),
    ("cv2", "opencv-python", "lectura de imágenes y filtros"),
    ("skimage", "scikit-image", "watershed, morfología, Otsu"),
    ("matplotlib", "matplotlib", "figuras de pasos intermedios"),
    ("pandas", "pandas", "tablas de resultados por imagen y método"),
]
URL_CFD = "https://github.com/cuilimeng/CrackForest-dataset/archive/refs/heads/master.zip"
URL_DEEPCRACK ="https://github.com/yhlleo/DeepCrack/raw/master/dataset/DeepCrack.zip"


def titulo(texto):
    print("\n" + "=" * 64 + f"\n{texto}\n" + "=" * 64)


def revisar_librerias(lista):
    """Devuelve la lista de paquetes pip que faltan."""
    faltan = []
    for modulo, paquete_pip, uso in lista:
        try:
            m = importlib.import_module(modulo)
            version = getattr(m, "__version__", "instalada")
            print(f"  [OK]    {modulo:12s} {version:12s} ({uso})")
        except ImportError:
            print(f"  [FALTA] {modulo:12s} {'':12s} ({uso})")
            faltan.append(paquete_pip)
    return faltan


def descargar(url, destino):
    print(f"  Descargando {url}\n  -> {destino}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_suffix(destino.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as r, open(temporal, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        leido = 0
        while bloque := r.read(1 << 20):
            f.write(bloque)
            leido += len(bloque)
            if total:
                print(f"\r  {leido / 1e6:6.1f} / {total / 1e6:.1f} MB", end="")
    print()
    temporal.replace(destino)


def descargar_cfd(carpeta):
    # Descarga CrackForest desde GitHub y copia image/, groundTruth/ y seg/ en data/.
    zip_local = RAIZ / "CrackForest.zip"
    try:
        descargar(URL_CFD, zip_local)
    except Exception as e:  # noqa: BLE001
        print(f"  [ERROR] Descarga fallida: {e}\n"
              f"  Descárgalo a mano desde {URL_CFD} y guárdalo como {zip_local};\n"
              f"  luego vuelve a ejecutar este script.")
        return False
    print("  Descomprimiendo...")
    with zipfile.ZipFile(zip_local) as z:
        for nombre in z.namelist():
            partes = Path(nombre).parts       # p. ej. CrackForest-dataset-master/image/001.jpg
            if len(partes) >= 3 and partes[1] in ("image", "groundTruth", "seg") and not nombre.endswith("/"):
                destino = carpeta / partes[1] / Path(*partes[2:])
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(z.read(nombre))
    zip_local.unlink()
    return True


def revisar_cfd():
    carpeta = RAIZ / "data"
    if not list((carpeta / "groundTruth").glob("*.mat")):
        print("  CrackForest no está en data/ (normal si se ejecuta en otro equipo). Se descarga...")
        if not descargar_cfd(carpeta):
            return False
    gts = sorted((carpeta / "groundTruth").glob("*.mat"))
    imgs = {p.stem for p in (carpeta / "image").glob("*.jpg")}
    con_par = [g for g in gts if g.stem in imgs]
    if not gts:
        print("  [ERROR] No se encontró data/groundTruth/*.mat. Revisa la carpeta data/.")
        return False
    print(f"  [OK] CFD: {len(imgs)} imágenes, {len(gts)} ground truth, "
          f"{len(con_par)} pares imagen + GT utilizables")
    try:
        import scipy.io as sio
        m = sio.loadmat(gts[0])["groundTruth"][0, 0]["Segmentation"]
        print(f"  [OK] Lectura de prueba {gts[0].name}: tamaño {m.shape}, "
              f"clases {sorted(set(m.ravel().tolist()))} (2 = fisura)")
    except Exception as e:  # noqa: BLE001
        print(f"  [AVISO] No se pudo leer {gts[0].name}: {e}")
    return True


def preparar_deepcrack():
    carpeta = RAIZ / "data_deepcrack"
    if (carpeta / "test_img").is_dir() and (carpeta / "test_lab").is_dir():
        print("  [OK] DeepCrack ya está en data_deepcrack/ (no se descarga de nuevo)")
    else:
        zip_local = carpeta / "DeepCrack.zip"
        if not zip_local.exists():
            try:
                descargar(URL_DEEPCRACK, zip_local)
            except Exception as e:  # noqa: BLE001
                print(f"  [ERROR] Descarga fallida: {e}\n"
                      f"  Descárgalo a mano desde {URL_DEEPCRACK}\n"
                      f"  y guárdalo como {zip_local}; luego vuelve a ejecutar este script.")
                return False
        print("  Descomprimiendo...")
        with zipfile.ZipFile(zip_local) as z:
            z.extractall(carpeta)
        zip_local.unlink()
    n = {d: len(list((carpeta / d).glob("*"))) for d in ["train_img", "train_lab", "test_img", "test_lab"]}
    print(f"  [OK] DeepCrack: train {n['train_img']} img / {n['train_lab']} GT; "
          f"test {n['test_img']} img / {n['test_lab']} GT")
    return True


def main():
    titulo("1. Entorno de Python")
    print(f"  Python {sys.version.split()[0]}  ->  {sys.executable}")
    if sys.prefix == sys.base_prefix:
        print("  [AVISO] No hay un entorno virtual activo. Si usa uno (p. ej. .venv), actívelo;\n"
              "          si trabaja con su Python global, puede ignorar este aviso.")
    if sys.version_info < (3, 10):
        print("  [AVISO] Se requiere Python 3.10 o superior (NumPy 2).")

    titulo("2. Librerías del núcleo (Actividad 2)")
    faltan = revisar_librerias(NUCLEO)

    titulo("3. Dataset CrackForest (carpeta data/)")
    ok_cfd = revisar_cfd()

    titulo("4. Dataset DeepCrack (carpeta data_deepcrack/)")
    ok_dc = preparar_deepcrack()

    titulo("5. Carpeta de resultados")
    (RAIZ / "resultados_act2").mkdir(exist_ok=True)
    print("  [OK] resultados_act2/ lista")

    titulo("RESUMEN")
    if faltan:
        print("  Instala lo que falta con:\n    pip install -r requirements.txt")
    libre = shutil.disk_usage(RAIZ).free / 1e9
    print(f"  Espacio libre en disco: {libre:.1f} GB")
    if not faltan and ok_cfd and ok_dc:
        print("  Todo listo para la Actividad 2.")
    else:
        print("  Corrige los puntos marcados y vuelve a ejecutar este script.")


if __name__ == "__main__":
    main()
