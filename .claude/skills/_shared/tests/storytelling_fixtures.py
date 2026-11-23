"""Proyecto de ejemplo del paso 10-make-storytelling: los capítulos 1 y 2 y la corrida de 09 de dashboard_fixtures, y una corrida de 10
armada con el ejemplo de su plantilla y las capturas copiadas de 09."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_fixtures as DF  # noqa: E402
import projectcfg as P  # noqa: E402

PASO = "10-make-storytelling"
RUN = "17-11-2026-08-00-00"
MODELOS = DF.F.COMMON / "10-storytelling" / "models"


def corrida(raiz, run9, registrar=True):
    """Escribe la corrida de 10 con el ejemplo de st-1 y las capturas de 09; la registra y devuelve su carpeta."""
    run = Path(raiz) / "project" / "10-storytelling" / RUN
    (run / "secciones").mkdir(parents=True)
    (run / "capturas").mkdir()
    (run / "secciones" / "4.md").write_text(DF.F.ejemplo(MODELOS / "st-1-seccion-4.md"), encoding="utf-8")
    for png in sorted((Path(run9) / "capturas").glob("*.png")):
        shutil.copyfile(png, run / "capturas" / png.name)
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if registrar:
        P.register(PASO, RUN, root=raiz)
    return run


def crear(raiz, registrar=True):
    """Capítulos 1 y 2, la corrida de 09 y la de 10; devuelve (corrida de 10, corrida de 09, corridas de 03 a 07)."""
    run9, runs = DF.crear(raiz)
    return corrida(raiz, run9, registrar), run9, runs
