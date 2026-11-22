"""Proyecto de ejemplo de los capítulos 1 y 2: brief, domain.md y corridas de 03 a 07 armadas con los ejemplos de las plantillas."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brief_fixtures as BF  # noqa: E402
import html_tpl as H  # noqa: E402
import projectcfg as P  # noqa: E402
import visuales as VI  # noqa: E402

COMMON = HERE.parents[2] / "common"
RUNS = {"03-make-business-diagnosis": "11-11-2026-08-00-00", "04-make-strategic-analysis": "12-11-2026-08-00-00",
        "05-make-problem-objectives": "13-11-2026-08-00-00", "06-make-bi-solution": "14-11-2026-08-00-00",
        "07-make-data-model-kpi": "15-11-2026-08-00-00"}
MODELOS = {
    "03-make-business-diagnosis": ("03-business-diagnosis", {"1.1": "bd-1-empresa.md", "1.2": "bd-2-mision-vision.md",
                                                             "1.3": "bd-3-industria-tamano.md", "1.4": "bd-4-canvas.md"}),
    "04-make-strategic-analysis": ("04-strategic-analysis", {"1.5": "sa-1-pestel.md", "1.6": "sa-2-foda.md", "1.7": "sa-3-ishikawa.md"}),
    "05-make-problem-objectives": ("05-problem-objectives", {"1.8": "po-1-problematica.md", "1.9": "po-2-objetivo-general.md",
                                                             "1.10": "po-3-objetivos-especificos.md"}),
    "06-make-bi-solution": ("06-bi-solution", {"2.1": "bs-1-propuesta.md", "2.2": "bs-2-arquitectura.md", "2.3": "bs-3-herramientas.md"}),
    "07-make-data-model-kpi": ("07-data-model-kpi", {"2.4": "dm-1-modelo.md", "2.5": "dm-2-kpi.md"}),
}

DOMAIN = """# Dominio del proyecto

Tipo: propio (empresa planteada por el equipo, sin RUC)

## Datos generales
| Dato | Valor |
|---|---|
| Nombre comercial | Pollería Don Tito (modelado por el agente, por no contar con un nombre registrado) |
| Actividad económica | Restaurantes (CIIU 5610) |
| Industria (CIIU) | 5610 |
| Tamaño (según ventas anuales y trabajadores) | Pequeña empresa |
| Locales y canales | Zárate y Canto Grande |

## Descripción de la empresa
Restaurante de pollo a la brasa con dos locales en San Juan de Lurigancho.

## Misión
Servir el mejor pollo a la brasa de San Juan de Lurigancho, con sabor casero, atención rápida y precios justos para las familias del distrito, en el local o en su casa. (modelado por el agente, por no contar con una misión publicada)

## Visión
Al 2029, ser la pollería de referencia de Lima Este, con cuatro locales y una operación rentable guiada por datos.

## Valores
- Sabor casero y constante.

## Clientes y competencia
Familias del distrito; cadenas y pollerías independientes.

## Contexto del proyecto
Gerencia y cocina usarán el dashboard.
"""


def ejemplo_json(ruta):
    """Último bloque ```json de una plantilla."""
    t = Path(ruta).read_text(encoding="utf-8")
    return re.findall(r"```json\n(.*?)```", t, flags=re.S)[-1].strip() + "\n"


def ejemplo(ruta):
    """Último bloque ```markdown de una plantilla."""
    t = Path(ruta).read_text(encoding="utf-8")
    return re.findall(r"```markdown\n(.*?)```", t, flags=re.S)[-1].strip() + "\n"


def base(raiz):
    """Config, brief vigente y domain.md del caso de ejemplo."""
    BF.crear(raiz, domain=False)
    (Path(raiz) / "project" / "domain.md").write_text(DOMAIN, encoding="utf-8")


def corrida(raiz, paso, registrar=True, visuales=True):
    """Escribe la corrida de `paso` con los ejemplos de sus plantillas, construye sus visuales y la registra."""
    carpeta, modelos = MODELOS[paso]
    run = Path(raiz) / "project" / carpeta / RUNS[paso]
    (run / "secciones").mkdir(parents=True)
    for punto, archivo in modelos.items():
        (run / "secciones" / f"{punto}.md").write_text(ejemplo(COMMON / carpeta / "models" / archivo), encoding="utf-8")
    readme = COMMON / carpeta / "models" / "README.md"
    if "```markdown" in readme.read_text(encoding="utf-8"):
        (run / "referencias.md").write_text(ejemplo(readme), encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if paso == "07-make-data-model-kpi":
        (run / "modelo.json").write_text(ejemplo_json(COMMON / carpeta / "models" / "dm-3-modelo-json.md"), encoding="utf-8")
    if visuales:
        construir(raiz, paso, run)
    if registrar:
        P.register(paso, RUNS[paso], root=raiz)
    return run


INTERPRETACION = ("Lo que debes entender es el cruce de los datos del caso y no cada pieza por separado. "
                  "La figura muestra dónde se pierde el margen y qué parte depende del negocio. "
                  "Por eso las decisiones del proyecto parten de ella.")


def construir(raiz, paso, run):
    tk = H.cargar_tokens(None, "base")
    for v, (_, origen, _) in VI.VISUALES.items():
        if origen == paso:
            VI.construir(v, raiz, Path(run) / "visuales", tk, run=Path(run).name, interpretacion=INTERPRETACION)


def crear(raiz, hasta="05-make-problem-objectives"):
    """Proyecto con las corridas de 03 hasta `hasta` registradas; devuelve {paso: carpeta}."""
    base(raiz)
    out = {}
    for paso in MODELOS:
        out[paso] = corrida(raiz, paso)
        if paso == hasta:
            break
    return out
