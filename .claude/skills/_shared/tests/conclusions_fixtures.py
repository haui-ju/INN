"""Proyecto de ejemplo del paso 11-make-conclusions: los capítulos 1 y 2 y la corrida de 09 (con sus valores) de dashboard_fixtures
más una corrida de 11 armada con el ejemplo de su plantilla, y una corrida mínima de 10 para los hallazgos que cita."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_fixtures as DF  # noqa: E402
import diagnostico_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402

PASO = "11-make-conclusions"
PASO10 = "10-make-storytelling"
RUN = "17-11-2026-08-00-00"
MODELOS = F.COMMON / "11-conclusions" / "models"
HALLAZGOS = """## 4. Storytelling con datos

Los hallazgos se basan en datos generados para el proyecto.

Tabla 1: Hallazgos del dashboard

| Código | Objetivo | KPI | Hallazgo |
|---|---|---|---|
| HLZ-01 | OE-01 | KPI-01 | La calidad de datos quedó por debajo de su meta. |
| HLZ-02 | OE-03 | KPI-03 | La merma por turno duplica la meta. |
"""


def crear(raiz, registrar=True):
    """Capítulos 1 y 2, la corrida de 09 y la de 11; devuelve (corrida de 11, corrida de 09, runs de 03 a 07)."""
    run09, runs = DF.crear(raiz)
    run = Path(raiz) / "project" / "11-conclusions" / RUN
    (run / "secciones").mkdir(parents=True)
    (run / "secciones" / "5.md").write_text(F.ejemplo(MODELOS / "cn-1-seccion-5.md"), encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if registrar:
        P.register(PASO, RUN, root=raiz)
    return run, run09, runs


def crear10(raiz, registrar=True):
    """Corrida mínima de 10-make-storytelling con la sección 4 (solo para comprobar los HLZ-nn que cita la sección 5)."""
    run = Path(raiz) / "project" / "10-storytelling" / "16-11-2026-09-00-00"
    (run / "secciones").mkdir(parents=True)
    (run / "secciones" / "4.md").write_text(HALLAZGOS, encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if registrar:
        P.register(PASO10, run.name, root=raiz)
    return run
