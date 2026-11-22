"""Proyecto de ejemplo del capítulo 3 (dashboard): los capítulos 1 y 2 de diagnostico_fixtures más una corrida de 09-make-dashboard
armada con los ejemplos de sus plantillas, con las capturas y los valores que entrega el equipo."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402

PASO = "09-make-dashboard"
RUN = "16-11-2026-08-00-00"
MODELOS = F.COMMON / "09-dashboard" / "models"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16


def ejemplo4(ruta):
    """Último bloque de cuatro comillas ````markdown de una plantilla (el ejemplo, cuando lleva bloques de código dentro)."""
    t = Path(ruta).read_text(encoding="utf-8")
    return re.findall(r"````markdown\n(.*?)````", t, flags=re.S)[-1].strip() + "\n"


def crear(raiz, registrar=True, capturas=True):
    """Capítulos 1 y 2 de ejemplo y la corrida de 09 con sus entradas; devuelve la carpeta de la corrida de 09 (los de 03 a 07 en `runs`)."""
    runs = F.crear(raiz, hasta="07-make-data-model-kpi")
    run = Path(raiz) / "project" / "09-dashboard" / RUN
    (run / "secciones").mkdir(parents=True)
    (run / "anexos").mkdir()
    (run / "secciones" / "3.2.md").write_text(F.ejemplo(MODELOS / "ds-1-paginas.md"), encoding="utf-8")
    (run / "anexos" / "C.md").write_text(ejemplo4(MODELOS / "ds-2-medidas.md"), encoding="utf-8")
    (run / "anexos" / "D.md").write_text(F.ejemplo(MODELOS / "ds-3-especificacion.md"), encoding="utf-8")
    (run / "valores.json").write_text(F.ejemplo_json(MODELOS / "ds-4-valores-json.md"), encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if capturas:
        (run / "capturas").mkdir()
        for n in range(1, 5):
            (run / "capturas" / f"pag-{n:02d}.png").write_bytes(PNG)
    if registrar:
        P.register(PASO, RUN, root=raiz)
    return run, runs
