"""Proyecto con corridas de 03, 04 y 05 escritas según el contrato de corrida del informe (spec report-assembly).

Cada corrida trae secciones/<punto>.md, marcas `<!-- figura: <visual> -->` con visuales/<visual>.html y
leer-imagen/<visual>.md, referencias.md y README.md, y se registra con projectcfg.register.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brief_fixtures as BF  # noqa: E402
import projectcfg as P  # noqa: E402

DIAG, ESTR, OBJ = "03-make-business-diagnosis", "04-make-strategic-analysis", "05-make-problem-objectives"
ETL, DASH = "08-make-etl", "09-make-dashboard"
RUN = "21-11-2026-10-00-00"

REF_KOTLER = "Kotler, P., & Keller, K. L. (2016). *Marketing management* (15.ª ed.). Pearson."
REF_OSTER = "Osterwalder, A., & Pigneur, Y. (2010). *Business model generation*. John Wiley & Sons."
REF_ISHI = "Ishikawa, K. (1986). *Guide to quality control*. Asian Productivity Organization."

SECCIONES = {
    DIAG: {
        "1.1": "## 1.1. Nombre de la empresa\n\nPollería Don Tito es un restaurante de pollo a la brasa con dos locales en San Juan de Lurigancho.\n",
        "1.2": "## 1.2. Misión y visión\n\n**Misión.** Servir pollo a la brasa de calidad a precio justo.\n\n**Visión.** Ser la pollería preferida del distrito al 2028.\n",
        "1.3": ("## 1.3. Industria y tamaño\n\nLa empresa pertenece al sector de restaurantes (CIIU 5610) y es una pequeña empresa.\n\n"
                "Tabla 1: Datos del sector\n\n| Indicador | Valor |\n|---|---|\n| Locales | 2 |\n| Trabajadores | 18 |\n\n"
                "La Tabla 1 resume el tamaño de la empresa según sus registros de 2026.\n"),
        "1.4": ("## 1.4. Modelo de negocio con el lienzo\n\nEl lienzo resume cómo la pollería crea y captura valor.\n\n"
                "<!-- figura: bmc -->\n\nLa Figura 1 muestra los nueve bloques (Osterwalder y Pigneur, 2010).\n\n### Propuesta de valor\n\nPollo a la brasa con receta propia.\n"),
    },
    ESTR: {
        "1.5": "## 1.5. Análisis PESTEL\n\nEl entorno combina alzas del insumo y más pedidos por aplicativo.\n\n<!-- figura: pestel -->\n",
        "1.6": ("## 1.6. Matriz FODA\n\nLa matriz cruza los factores internos y externos (Kotler y Keller, 2016).\n\n<!-- figura: foda -->\n\n"
                "Tabla 1: Estrategias cruzadas\n\n| Código | Estrategia |\n|---|---|\n| FO-01 | Precio diferenciado por canal |\n"),
        "1.7": "## 1.7. Diagrama de Ishikawa\n\nLas causas se agrupan por categoría (Ishikawa, 1986).\n\n<!-- figura: ishikawa -->\n",
    },
    OBJ: {
        "1.8": "## 1.8. Problemática central del negocio\n\nEl margen neto cayó de 14 % a 8 % en 2026 mientras las ventas crecieron 18 %, como muestra la {{figura:foda}}.\n",
        "1.9": "## 1.9. Objetivo general del proyecto\n\nOG-01: recuperar el margen neto de 12 % al cierre del proyecto.\n",
        "1.10": "## 1.10. Objetivos específicos\n\n| Código | Objetivo | Indicador |\n|---|---|---|\n| OE-01 | Medir el margen por canal | Margen por canal |\n",
    },
}

LEER = {
    "bmc": "# Cómo leer la figura bmc\n\n- **Para qué sirve.** Resume el modelo de negocio en nueve bloques.\n- **Qué dice.** El canal de delivery concentra el crecimiento\n- **Pie de foto sugerido.** Business Model Canvas de Pollería Don Tito\n",
    "foda": ("# Cómo leer la figura foda\n\n- **Para qué sirve.** Cruza fortalezas y debilidades con oportunidades y amenazas.\n"
             "- **Qué dice.** La receta propia compensa la presión del costo del pollo.\n- **Por qué se resalta.** La amenaza del insumo se marca en rojo.\n"
             "- **Pie de foto sugerido.** Matriz FODA de Pollería Don Tito.\n"),
    "ishikawa": "- **Para qué sirve:** Ordena las causas del margen bajo.\n- **Qué dice:** El precio único por canal es la causa principal.\n- **Pie de foto sugerido:** Diagrama de Ishikawa del margen neto\n",
}
VISUALES = {DIAG: ["bmc"], ESTR: ["pestel", "foda", "ishikawa"]}
REFERENCIAS = {DIAG: [REF_OSTER, REF_KOTLER], ESTR: [f"- {REF_KOTLER}", REF_ISHI, ""]}


def html_visual(nombre):
    return f"<!doctype html>\n<html lang=\"es\"><head><meta charset=\"utf-8\"><title>{nombre}</title></head><body><main>{nombre}</main></body></html>\n"


def corrida(raiz, skill, secciones, visuales=(), leer=None, referencias=None, anexos=None, registrar=True, run=RUN):
    """Escribe una corrida de contenido según el contrato y la registra; devuelve su carpeta."""
    d = P.run_dir(skill, run, raiz)
    (d / "secciones").mkdir(parents=True, exist_ok=True)
    for punto, texto in secciones.items():
        (d / "secciones" / f"{punto}.md").write_text(texto, encoding="utf-8")
    for v in visuales:
        (d / "visuales").mkdir(exist_ok=True)
        (d / "visuales" / f"{v}.html").write_text(html_visual(v), encoding="utf-8")
    for v, t in (leer or {}).items():
        (d / "leer-imagen").mkdir(exist_ok=True)
        (d / "leer-imagen" / f"{v}.md").write_text(t, encoding="utf-8")
    if referencias:
        (d / "referencias.md").write_text("\n".join(referencias) + "\n", encoding="utf-8")
    for letra, t in (anexos or {}).items():
        (d / "anexos").mkdir(exist_ok=True)
        (d / "anexos" / f"{letra}.md").write_text(t, encoding="utf-8")
    (d / "README.md").write_text(f"# Procedencia\n\nCorrida de {skill} escrita por la prueba (no debe copiarse al informe).\n", encoding="utf-8")
    if registrar:
        P.register(skill, run, root=raiz)
    return d


def crear(raiz, skills=(DIAG, ESTR, OBJ)):
    """Config, brief vigente y corridas de las skills pedidas (por omisión 03, 04 y 05)."""
    raiz = Path(raiz)
    (raiz / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
    BF.crear(raiz)
    dirs = {}
    for s in skills:
        leer = {v: LEER[v] for v in VISUALES.get(s, []) if v in LEER}
        dirs[s] = corrida(raiz, s, SECCIONES[s], VISUALES.get(s, []), leer, REFERENCIAS.get(s))
    return dirs
