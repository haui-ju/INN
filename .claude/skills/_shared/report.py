#!/usr/bin/env python3
"""Armado del informe de Inteligencia de Negocios (una sola entrega) con las secciones disponibles del config.

  python3 .claude/skills/_shared/report.py plan      [--json] [--raiz .]
  python3 .claude/skills/_shared/report.py construir --salida RUN [--curso "..."] [--docente "..."] [--raiz .]
  python3 .claude/skills/_shared/report.py render    RUN/informe.md [--raiz .]
  python3 .claude/skills/_shared/report.py anexos    [--run CORRIDA] [--comprobar] [--raiz .]

`plan` muestra qué sección sale de qué corrida, las pendientes con la skill que las produce, los anexos y las figuras.
`construir` escribe en RUN (creada con runs.py new): informe.md, faltantes.md, README.md, imagenes/ (HTML de cada figura e
INDICE.md) y anexos/ si hay alguno. Solo entran las secciones `disponible` de informe.secciones, en el orden del índice
(common/structure/model1.md). Cada corrida de contenido aporta secciones/<punto>.md, marcas `<!-- figura: <visual> -->` con
visuales/<visual>.html y leer-imagen/<visual>.md, referencias.md opcional y anexos/<letra>.md. `render` escribe informe.html
con el sistema de diseño del config. `anexos` convierte a HTML los anexos de la corrida vigente (skill 13-make-annex-html).
Solo biblioteca estándar. PROJECT_ROOT o --raiz cambian la raíz (pruebas).
"""
import argparse
import html
import json
import os
import re
import shutil
import sys
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMON = HERE.parents[2] / "common"
INDICE = COMMON / "structure" / "model1.md"
MODELOS = COMMON / "12-report" / "models"
sys.path.insert(0, str(HERE))
import doc_html as DH  # noqa: E402
import projectcfg as P  # noqa: E402

PASO = "12-make-report"
CARPETA = "12-report"
INFORME = "informe.md"
PENDIENTE = "Pendiente"
NOMBRE_ANEXOS = "Anexos del informe"
MARCA_IMAGEN = "(incluye imagen)"
# Sección de origen de cada anexo: el anexo sale de anexos/<letra>.md de la corrida que produce esa sección.
ANEXOS_ORIGEN = {"A": "3.1", "B": "3.1", "C": "3.2", "D": "3.2"}

RE_CAP = re.compile(r"^## Capítulo (\d+): (.+?)\s*$")
RE_PUNTO = re.compile(r"^- (\d+(?:\.\d+)?)\. (.+?)\s*$")
RE_ANEXO = re.compile(r"^- Anexo ([A-Z]): (.+?)\s*$")
RE_HEAD = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
RE_FIGURA = re.compile(r"^\s*<!--\s*figura:\s*([A-Za-z0-9][\w-]*)\s*-->\s*$")
RE_CAPTURA = re.compile(r"^\s*<!--\s*captura:\s*([A-Za-z0-9][\w-]*)\s*-->\s*$")
RE_REF_FIGURA = re.compile(r"\{\{figura:([A-Za-z0-9][\w-]*)\}\}")
RE_MENCION = re.compile(r"\b(Figura|Tabla) (\d+)\b")
RE_TITULO_TABLA = re.compile(r"^(\*\*)?Tabla (\d+)([.:])")
RE_VINETA = re.compile(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*(.*)$")
MARCADOR = re.compile(r"^\(INCLUIR IMAGEN: Figura (\d+): (.+?)\. Archivo sugerido: (\S+?)\)\s*$")
COMO_COPIAR = "**Cómo copiarla.**"
COMO_LEER = "**Cómo leer la figura.**"
PIE = "Pie de foto sugerido"
ROTULOS_LECTURA = ("Para qué sirve", "Qué dice", "Por qué se resalta", "Qué debes entender")
ENTIENDE, DICE = "Qué debes entender", "Qué dice"
# Tablas que repiten por completo lo que ya muestra la figura: se quitan del informe armado cuando la figura está. Siguen en la
# sección de origen, porque de ellas sale el dibujo. Las demás (FODA con su evidencia, causas del Ishikawa, hechos y dimensiones) traen datos que la imagen no muestra.
TABLAS_EN_FIGURA = {
    "Bloques del Business Model Canvas": "bmc",
    "Componentes de la arquitectura de BI": "arquitectura-bi",
    "Relaciones del modelo": "modelo-datos",
}
FORMATO = ("**Formato de entrega.** Word o PDF, letra Arial 11, interlineado 1.5 y márgenes estándar. Antes de entregar, "
           "cada marcador «(INCLUIR IMAGEN: …)» se reemplaza por su imagen; el dashboard se presenta en Power BI en la exposición.")


QUE_HACER_PORTADA = {"Curso": "indícalo al armar el informe (`--curso`)", "Docente": "indícalo al armar el informe (`--docente`)",
                     "Tema": "complétalo con 01-make-project-brief-update", "Empresa": "complétalo con 01-make-project-brief-update",
                     "Fecha de entrega": "complétala con 01-make-project-brief-update", "Integrantes": "agrégalos con 00-init-update",
                     "Título del proyecto": "complétalo con 00-init-update"}


class ReportError(Exception):
    pass


# ---------------------------------------------------------------- índice
def _sin_detalle(t):
    """Quita la marca de imagen y el detalle final entre paréntesis: «Matriz FODA (fortalezas, …) (incluye imagen)» -> «Matriz FODA»."""
    t = t.replace(MARCA_IMAGEN, "").strip()
    detalle = ""
    if t.endswith(")"):
        nivel = 0
        for k in range(len(t) - 1, -1, -1):
            nivel += {")": 1, "(": -1}.get(t[k], 0)
            if nivel == 0:
                detalle, t = t[k + 1:-1].strip(), t[:k].strip()
                break
    return t, detalle


def cargar_indice():
    """Capítulos, puntos y anexos del índice maestro.

    {"caps": {1: título}, "puntos": {punto: {titulo, detalle, imagen, capitulo}}, "anexos": {letra: {titulo, detalle, origen}}}
    `imagen` es verdadero si la línea del punto lleva «(incluye imagen)».
    """
    caps, puntos, anexos, cap = {}, {}, {}, None
    for linea in INDICE.read_text(encoding="utf-8").splitlines():
        m = RE_CAP.match(linea)
        if m:
            cap = int(m.group(1))
            caps[cap] = m.group(2)
            continue
        if linea.startswith("## "):
            cap = None
        m = RE_ANEXO.match(linea)
        if m:
            titulo, detalle = _sin_detalle(m.group(2))
            anexos[m.group(1)] = {"titulo": titulo, "detalle": detalle, "origen": ANEXOS_ORIGEN.get(m.group(1))}
            continue
        m = RE_PUNTO.match(linea)
        if m and cap is not None:
            titulo, detalle = _sin_detalle(m.group(2))
            puntos[m.group(1)] = {"titulo": titulo, "detalle": detalle, "imagen": MARCA_IMAGEN in linea, "capitulo": cap}
    return {"caps": caps, "puntos": puntos, "anexos": anexos}


def introducciones():
    """{capítulo: frase} de common/12-report/models/rep-1-introducciones.md (tabla «| Capítulo | Introducción |»)."""
    f = MODELOS / "rep-1-introducciones.md"
    out = {}
    if not f.is_file():
        return out
    texto = f.read_text(encoding="utf-8").split("## Formato", 1)[0]
    for linea in texto.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", linea)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


# ---------------------------------------------------------------- utilidades
def _enumerar(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def _frase(t):
    t = t.strip()
    return t if not t or t.endswith((".", "!", "?", ":")) else t + "."


def _clave_orden(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", "", t)


def _norm(t):
    return re.sub(r"\s+", " ", (t or "").strip())


def _pendiente(v):
    v = _norm(v)
    return not v or v.lower().startswith(PENDIENTE.lower())


def fuera_de_codigo(lineas):
    """Índices de las líneas que no están dentro de un bloque ``` (allí no se interpretan marcas ni encabezados)."""
    dentro, out = False, []
    for k, l in enumerate(lineas):
        if l.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            out.append(k)
    return set(out)


def leer_imagen(f):
    """[(rótulo, texto)] de las viñetas «- **Rótulo.** texto» de leer-imagen/<visual>.md; None si no existe."""
    if f is None or not Path(f).is_file():
        return None
    out = []
    for l in Path(f).read_text(encoding="utf-8").splitlines():
        m = RE_VINETA.match(l)
        if m:
            rotulo = m.group(1).strip().rstrip(".:").strip()
            texto = m.group(2).strip().lstrip(".:").strip()
            if texto:
                out.append((rotulo, texto))
    return out


def como_leer(vinetas):
    """Párrafo «Cómo leer la figura.» con las viñetas de explicación (sin el pie); None si no hay ninguna."""
    partes = []
    hay_entiende = any(r == ENTIENDE for r, _ in vinetas or [])
    for rotulo, texto in vinetas or []:
        # «Qué dice» cuenta lo que se ve; cuando la skill redactó qué debe entender el lector, esa conclusión lo reemplaza.
        if rotulo == PIE or (hay_entiende and rotulo == DICE):
            continue
        partes.append(_frase(texto) if rotulo in ROTULOS_LECTURA else _frase(f"{rotulo}: {texto}"))
    return f"{COMO_LEER} " + " ".join(partes) if partes else None


def pie_de(vinetas, defecto):
    for rotulo, texto in vinetas or []:
        if rotulo == PIE:
            # leer-imagen sugiere «Figura X: Título»; el marcador ya lleva el número, así que se quita el prefijo.
            return re.sub(r"^Figura\s+X\s*:\s*", "", texto.strip().rstrip(".").strip(), flags=re.I)
    return defecto


def marcador(n, pie, visual):
    return marcador_archivo(n, pie, f"imagenes/{visual}.html")


def marcador_archivo(n, pie, ruta):
    return f"(INCLUIR IMAGEN: Figura {n}: {pie}. Archivo sugerido: {ruta})"


# ---------------------------------------------------------------- plan
def _anexo_de(run_dir, letra):
    for nombre in (f"{letra}.md", f"{letra.lower()}.md"):
        f = run_dir / "anexos" / nombre
        if f.is_file():
            return f
    return None


def _figuras(texto):
    lin = texto.splitlines()
    vivas = fuera_de_codigo(lin)
    return [RE_FIGURA.match(l).group(1) for k, l in enumerate(lin) if k in vivas and RE_FIGURA.match(l)]


def _brief(raiz):
    import brief as BR
    try:
        return BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError, OSError):
        return None


def plan(raiz=None):
    """Qué entra en el informe y qué falta, sin escribir nada."""
    raiz = P.repo_root(raiz)
    cfg = P.load(raiz)
    idx = cargar_indice()
    estado = {x["seccion"]: x for x in P.secciones(raiz)}
    incluidas, pendientes = [], []
    for punto, d in idx["puntos"].items():
        e = estado.get(punto)
        if e is None:
            pendientes.append({"seccion": punto, "titulo": d["titulo"], "skill": None, "motivo": "no figura en informe.secciones del config"})
            continue
        if e["estado"] != "disponible":
            pendientes.append({"seccion": punto, "titulo": d["titulo"], "skill": e["skill"], "motivo": e["motivo"] or f"falta ejecutar {e['skill']}"})
            continue
        run = P.run_dir(e["skill"], e["run"], raiz)
        f = run / "secciones" / f"{punto}.md"
        if not f.is_file():
            pendientes.append({"seccion": punto, "titulo": d["titulo"], "skill": e["skill"],
                               "motivo": f"la corrida {e['run']} no tiene secciones/{punto}.md: ejecuta {e['skill']}-update"})
            continue
        incluidas.append({"seccion": punto, "titulo": d["titulo"], "skill": e["skill"], "run": e["run"], "dir": run, "archivo": f})
    por_seccion = {x["seccion"]: x for x in incluidas}
    skill_de = dict(P.secciones_pipeline())
    anexos, anexos_pend = [], []
    for letra, d in idx["anexos"].items():
        origen = d["origen"]
        skill = skill_de.get(origen)
        fuente = por_seccion.get(origen)
        f = _anexo_de(fuente["dir"], letra) if fuente else None
        if f is None:
            motivo = (f"la sección de origen {origen} está pendiente: ejecuta {skill}" if fuente is None
                      else f"la corrida {fuente['run']} no tiene anexos/{letra}.md: ejecuta {skill}-update")
            anexos_pend.append({"anexo": letra, "titulo": d["titulo"], "skill": skill, "motivo": motivo})
        else:
            anexos.append({"anexo": letra, "titulo": d["titulo"], "skill": skill, "run": fuente["run"], "dir": fuente["dir"], "archivo": f})
    figuras = []
    for x in incluidas + anexos:
        for v in _figuras(x["archivo"].read_text(encoding="utf-8")):
            figuras.append({"visual": v, "lugar": x.get("seccion") or f"Anexo {x['anexo']}", "skill": x["skill"],
                            "html": (x["dir"] / "visuales" / f"{v}.html").is_file(), "explicacion": (x["dir"] / "leer-imagen" / f"{v}.md").is_file()})
    corridas = []
    for x in incluidas:
        if (x["skill"], x["run"]) not in [(s, r) for s, r, _ in corridas]:
            corridas.append((x["skill"], x["run"], [y["seccion"] for y in incluidas if y["skill"] == x["skill"]]))
    return {"cfg": cfg, "idx": idx, "incluidas": incluidas, "pendientes": pendientes, "anexos": anexos, "anexos_pendientes": anexos_pend,
            "figuras": figuras, "corridas": corridas, "brief": _brief(raiz), "raiz": raiz}


# ---------------------------------------------------------------- armado
class _Estado:
    def __init__(self, salida):
        self.salida = Path(salida)
        self.figuras = 0
        self.tablas = 0
        self.visuales = {}      # visual -> número de figura
        self.imagenes = []      # (visual, n, lugar, skill)
        self.capturas = []      # (id, n, lugar, skill, ruta o None): imágenes que aporta el equipo, no se copian
        self.avisos = []
        self.fig_incompletas = []  # (n, visual, lugar, qué falta, qué hacer)


def _cuerpo(texto, punto, avisos, lugar):
    """Líneas del cuerpo de una sección o anexo sin su encabezado propio, con los subtítulos a partir del nivel 3."""
    lin = texto.strip("\n").splitlines()
    while lin and not lin[0].strip():
        lin.pop(0)
    vivas = fuera_de_codigo(lin)
    nivel_propio = None
    if lin and 0 in vivas:
        m = RE_HEAD.match(lin[0])
        if m and punto is not None and re.match(rf"^(?:Anexo\s+)?{re.escape(punto)}(?:[.:]|\s|$)", m.group(2)):
            nivel_propio = len(m.group(1))
            lin = lin[1:]
    if nivel_propio is None and punto is not None:
        avisos.append(f"{lugar}: el archivo no abre con el encabezado de su punto («## {punto}. …»); se usa el texto completo")
    vivas = fuera_de_codigo(lin)
    niveles = [len(RE_HEAD.match(l).group(1)) for k, l in enumerate(lin) if k in vivas and RE_HEAD.match(l)]
    base = (nivel_propio + 1) if nivel_propio else (min(niveles) if niveles else 3)
    out = []
    for k, l in enumerate(lin):
        m = RE_HEAD.match(l) if k in vivas else None
        if m:
            nivel = max(3, min(6, 3 + len(m.group(1)) - base))
            out.append("#" * nivel + " " + m.group(2))
        else:
            out.append(l)
    while out and not out[-1].strip():
        out.pop()
    return out


def _bloque_figura(st, n, visual, ctx, prefijo, copiar):
    run, skill, lugar, titulo = ctx["dir"], ctx["skill"], ctx["lugar"], ctx["titulo"]
    html_src = run / "visuales" / f"{visual}.html"
    vin = leer_imagen(run / "leer-imagen" / f"{visual}.md")
    out = [marcador(n, pie_de(vin, titulo), visual), ""]
    faltan = []
    if html_src.is_file():
        if copiar:
            d = st.salida / "imagenes"
            d.mkdir(parents=True, exist_ok=True)
            destino = d / f"{visual}.html"
            if destino.exists() and destino.read_bytes() != html_src.read_bytes():
                st.avisos.append(f"la figura «{visual}» de {lugar} tiene el mismo nombre que otra de distinto contenido; se conserva la primera")
            else:
                shutil.copyfile(html_src, destino)
        out += [f"{COMO_COPIAR} Abrir [imagenes/{visual}.html]({prefijo}{visual}.html) en el navegador, elegir la escala y pulsar "
                "«Copiar imagen» (o «Descargar imagen»); luego pegarla en el lugar del marcador.", ""]
    else:
        faltan.append("HTML")
        out += [f"{COMO_COPIAR} La figura «{visual}» no tiene HTML en la corrida de {skill}: ejecuta {skill}-update para generarlo "
                "o inserta una captura propia en el lugar del marcador.", ""]
    lectura = como_leer(vin)
    if lectura:
        out += [lectura, ""]
    else:
        faltan.append("explicación (leer-imagen)")
    if copiar:
        st.imagenes.append((visual, n, lugar, skill, html_src.is_file()))
        if faltan:
            que = " y ".join(faltan)
            st.fig_incompletas.append((n, visual, lugar, que, f"ejecuta {skill}-update"))
            st.avisos.append(f"la Figura {n} ({visual}) de {lugar}: falta {que}; ejecuta {skill}-update")
    return out


def _pie_captura(png, titulo):
    """Pie de una captura: primera línea de capturas/<id>.md (sin viñeta) o, si falta, el título de la sección."""
    f = png.with_suffix(".md")
    if f.is_file():
        for l in f.read_text(encoding="utf-8").splitlines():
            t = re.sub(r"^\s*(?:[-*#]+\s*)+", "", l).strip().rstrip(".")
            if t:
                return t
    return titulo


def _bloque_captura(st, n, id_, ctx, prefijo, copiar):
    """Marcador de una captura que aporta el equipo (capturas/<id>.png de la corrida de la sección). No se copia al informe."""
    run, skill, lugar, titulo = ctx["dir"], ctx["skill"], ctx["lugar"], ctx["titulo"]
    png = run / "capturas" / f"{id_}.png"
    pie = _pie_captura(png, titulo)
    if png.is_file():
        ruta = os.path.relpath(png, st.salida).replace(os.sep, "/")
        if prefijo.startswith("../"):
            ruta = "../" + ruta
        out = [marcador_archivo(n, pie, ruta), "",
               f"{COMO_COPIAR} Abrir [{ruta}]({ruta}) y pegar la imagen en el lugar del marcador.", ""]
        if copiar:
            st.capturas.append((id_, n, lugar, skill, ruta))
        return out
    out = [marcador_archivo(n, pie, f"capturas/{id_}.png"), "",
           f"{COMO_COPIAR} Falta la captura «{id_}»: guárdala en capturas/{id_}.png de la corrida de {skill} y vuelve a armar el informe.", ""]
    if copiar:
        st.capturas.append((id_, n, lugar, skill, None))
        st.fig_incompletas.append((n, id_, lugar, "captura", f"guarda capturas/{id_}.png en la corrida de {skill}"))
        st.avisos.append(f"la Figura {n} ({id_}) de {lugar}: falta la captura capturas/{id_}.png de la corrida de {skill}")
    return out


def _sin_tablas_de_la_figura(lineas, ctx):
    """Quita, con su título, las tablas de TABLAS_EN_FIGURA cuya figura está en el bloque y tiene su HTML."""
    vivas = fuera_de_codigo(lineas)
    figuras = {m.group(1) for k in vivas if (m := RE_FIGURA.match(lineas[k]))}
    quitar = set()
    for k in sorted(vivas):
        t = RE_TITULO_TABLA.match(lineas[k])
        if not t:
            continue
        titulo = re.sub(r"^\**Tabla \d+[.:]\s*", "", lineas[k]).strip(" *")
        visual = TABLAS_EN_FIGURA.get(titulo)
        if visual not in figuras or not (ctx["dir"] / "visuales" / f"{visual}.html").is_file():
            continue
        j = k + 1
        while j < len(lineas) and not lineas[j].strip():
            j += 1
        while j < len(lineas) and lineas[j].startswith("|"):
            j += 1
        quitar.update(range(k, j))
        if j < len(lineas) and not lineas[j].strip():
            quitar.add(j)
    return [l for i, l in enumerate(lineas) if i not in quitar]


def _procesar(st, lineas, ctx, prefijo="imagenes/", copiar=True):
    """Reemplaza las marcas de figura, renumera figuras y títulos de tabla y actualiza sus menciones en el bloque."""
    lineas = _sin_tablas_de_la_figura(lineas, ctx)
    vivas = fuera_de_codigo(lineas)
    figs = [k for k in sorted(vivas) if RE_FIGURA.match(lineas[k]) or RE_CAPTURA.match(lineas[k])]
    tits = [k for k in sorted(vivas) if RE_TITULO_TABLA.match(lineas[k])]
    mapa = {"Figura": {}, "Tabla": {}}
    for j, k in enumerate(figs, 1):
        mapa["Figura"][str(j)] = str(st.figuras + j)
    for j, k in enumerate(tits, 1):
        local = RE_TITULO_TABLA.match(lineas[k]).group(2)
        mapa["Tabla"].setdefault(local, str(st.tablas + j))
    # tablas sin título
    for k in sorted(vivas):
        if lineas[k].startswith("|") and (k == 0 or not lineas[k - 1].startswith("|")):
            previa = next((lineas[i] for i in range(k - 1, -1, -1) if lineas[i].strip()), "")
            if not RE_TITULO_TABLA.match(previa) and copiar:
                st.avisos.append(f"{ctx['lugar']}: hay una tabla sin título «Tabla N: …» (lo agrega la skill {ctx['skill']})")

    def mencion(m):
        nuevo = mapa[m.group(1)].get(m.group(2))
        if nuevo is None:
            if copiar:
                st.avisos.append(f"{ctx['lugar']}: menciona «{m.group(0)}», que no está en el mismo bloque; revisa la referencia")
            return m.group(0)
        return f"{m.group(1)} {nuevo}"

    out = []
    for k, l in enumerate(lineas):
        if k not in vivas:
            out.append(l)
            continue
        m = RE_FIGURA.match(l)
        c = None if m else RE_CAPTURA.match(l)
        if m or c:
            st.figuras += 1
            nombre = (m or c).group(1)
            if copiar:
                st.visuales.setdefault(nombre, st.figuras)
            if out and out[-1].strip():
                out.append("")
            out += (_bloque_figura if m else _bloque_captura)(st, st.figuras, nombre, ctx, prefijo, copiar)
            continue
        out.append(RE_MENCION.sub(mencion, l))
    st.tablas += len(tits)
    while out and not out[-1].strip():
        out.pop()
    return out


def _refs_figura(texto, st):
    def rep(m):
        n = st.visuales.get(m.group(1))
        if n is None:
            st.avisos.append(f"la referencia {{{{figura:{m.group(1)}}}}} no corresponde a ninguna figura del informe")
            return m.group(0)
        return f"Figura {n}"
    return RE_REF_FIGURA.sub(rep, texto)


def _referencias(corridas_dirs):
    vistas, out = set(), []
    for d in corridas_dirs:
        f = d / "referencias.md"
        if not f.is_file():
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            e = re.sub(r"^\s*[-*]\s+", "", l).strip()
            if not e or e.startswith("#"):
                continue
            k = _norm(e).lower()
            if k not in vistas:
                vistas.add(k)
                out.append(_norm(e))
    return sorted(out, key=_clave_orden)


def _control(cfg, br, curso, docente):
    p = cfg["proyecto"]
    equipo = [m["nombre"] + (f" ({m['rol']})" if m.get("rol") else "") for m in cfg.get("equipo", [])]
    empresa = (br or {}).get("empresa") or ""
    datos = [("Título del proyecto", p.get("nombre") or ""), ("Tema", p.get("tema") or ""), ("Empresa", empresa),
             ("Curso", curso or ""), ("Docente", docente or ""), ("Integrantes", ", ".join(equipo)),
             ("Fecha de entrega", (cfg.get("calendario") or {}).get("entrega") or "")]
    faltan = []
    filas = []
    for campo, valor in datos:
        if _pendiente(valor):
            faltan.append(campo)
            valor = PENDIENTE
        filas.append(f"| {campo} | {_norm(valor).replace('|', '/')} |")
    lineas = [f"# Informe · {p.get('nombre') or PENDIENTE}", "", "## Control del documento", "", "| Campo | Dato |", "|---|---|"] + filas + ["", FORMATO, ""]
    return lineas, faltan


def _tabla(cabecera, filas):
    t = ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    t += ["| " + " | ".join(str(c).replace("|", "/") for c in f) + " |" for f in filas] or ["| " + " | ".join("—" for _ in cabecera) + " |"]
    return t


def escribir_faltantes(pl, st, portada, sin_refs):
    t = ["# Faltantes del informe", "",
         "Lo que todavía no entra en `informe.md` y qué lo produce. Después de ejecutar la skill indicada, vuelve a armar el informe con `12-make-report`.", "",
         "## Secciones", ""]
    t += _tabla(["Sección", "Título", "Skill que la produce", "Causa"],
                [(x["seccion"], x["titulo"], x["skill"] or "—", x["motivo"]) for x in pl["pendientes"]])
    t += ["", "## Anexos", ""]
    t += _tabla(["Anexo", "Título", "Skill que lo produce", "Causa"],
                [(x["anexo"], x["titulo"], x["skill"] or "—", x["motivo"]) for x in pl["anexos_pendientes"]])
    t += ["", "## Datos de portada", ""]
    t += _tabla(["Dato", "Qué hacer"], [(c, QUE_HACER_PORTADA.get(c, "complétalo con 00-init-update")) for c in portada])
    t += ["", "## Figuras incompletas", ""]
    t += _tabla(["Figura", "Visual", "Lugar", "Qué falta", "Qué hacer"], [(f"Figura {n}", v, lugar, que, hacer) for n, v, lugar, que, hacer in st.fig_incompletas])
    t += ["", "## Referencias", "", ("Ninguna de las corridas usadas aporta `referencias.md`." if sin_refs else "Sin faltantes."), ""]
    return "\n".join(t)


def escribir_indice_imagenes(st):
    if not st.imagenes and not st.capturas:
        return
    d = st.salida / "imagenes"
    d.mkdir(parents=True, exist_ok=True)
    filas = []
    for visual, n, lugar, skill, hay in st.imagenes:
        archivo = f"[{visual}.html]({visual}.html)" if hay else f"{visual}.html (sin HTML: ejecuta {skill}-update)"
        filas.append((archivo, f"Figura {n}", lugar, skill))
    for id_, n, lugar, skill, ruta in st.capturas:
        archivo = f"[{id_}.png](../{ruta})" if ruta else f"{id_}.png (falta la captura: guárdala en la corrida de {skill})"
        filas.append((archivo, f"Figura {n}", lugar, skill))
    t = ["# Imágenes del informe", "",
         "Cada HTML de esta carpeta es una figura del informe. Ábrelo en el navegador, elige la escala y pulsa «Copiar imagen» "
         "(o «Descargar imagen»); luego pégala en el marcador «(INCLUIR IMAGEN: …)» de su figura. "
         "Las capturas del dashboard son imágenes del equipo: el enlace apunta a su archivo en la corrida que las produjo.", ""]
    t += _tabla(["Archivo", "Figura", "Dónde va", "Skill de origen"], filas)
    (d / "INDICE.md").write_text("\n".join(t) + "\n", encoding="utf-8")


def escribir_readme(pl, st, curso, docente, anexos):
    cfg = pl["cfg"]
    total = len(pl["idx"]["puntos"])
    t = ["# Procedencia del informe", "",
         f"- Armado el {time.strftime('%d-%m-%Y a las %H:%M')} con `12-make-report` (`report.py construir`).",
         f"- Modo de datos del config: {cfg.get('modo_datos')}.",
         f"- Sistema de diseño: {cfg.get('diseno') or 'tokens base (sin 02-design-system)'}.",
         f"- Brief: {'corrida vigente de 01-make-project-brief' if pl['brief'] else 'sin corrida vigente de 01-make-project-brief'}.",
         f"- Curso: {curso or PENDIENTE}. Docente: {docente or PENDIENTE}.",
         f"- Secciones incluidas: {len(pl['incluidas'])} de {total}; pendientes: {len(pl['pendientes'])} (ver `faltantes.md`).",
         f"- Anexos incluidos: {', '.join(a['anexo'] for a in anexos) or 'ninguno'}.",
         f"- Figuras: {st.figuras}; tablas con título: {st.tablas}.", "",
         "## Corridas usadas", ""]
    t += _tabla(["Skill", "Corrida", "Secciones"], [(s, r, ", ".join(secs)) for s, r, secs in pl["corridas"]])
    if st.avisos:
        t += ["", "## Avisos del armado", ""] + [f"- {a}" for a in st.avisos]
    return "\n".join(t) + "\n"


def armar(pl, salida, curso=None, docente=None):
    """(texto del informe, {letra: texto del anexo}, estado, datos de portada pendientes, sin referencias)."""
    st = _Estado(salida)
    idx = pl["idx"]
    intro = introducciones()
    lineas, portada = _control(pl["cfg"], pl["brief"], curso, docente)
    if pl["brief"] is None:
        st.avisos.append("no hay brief vigente (01-make-project-brief): la empresa queda «Pendiente»")
    por_cap = {}
    for x in pl["incluidas"]:
        por_cap.setdefault(idx["puntos"][x["seccion"]]["capitulo"], []).append(x)
    for cap, titulo_cap in idx["caps"].items():
        secs = por_cap.get(cap)
        if not secs:
            continue
        lineas += [f"# Capítulo {cap}: {titulo_cap}", ""]
        lista = _enumerar(f"{x['seccion']} {x['titulo']}" for x in secs)
        frase = intro.get(cap, "")
        lineas += [(_frase(frase) + " " if frase else "") + f"Comprende {lista}.", ""]
        for x in secs:
            d = idx["puntos"][x["seccion"]]
            lugar = f"la sección {x['seccion']}"
            cuerpo = _cuerpo(x["archivo"].read_text(encoding="utf-8"), x["seccion"], st.avisos, lugar)
            ctx = {"dir": x["dir"], "skill": x["skill"], "lugar": lugar, "titulo": d["titulo"]}
            antes = st.figuras
            cuerpo = _procesar(st, cuerpo, ctx)
            if d["imagen"] and st.figuras == antes:
                st.avisos.append(f"{lugar} lleva la marca «(incluye imagen)» en el índice y no trae ninguna figura: ejecuta {x['skill']}-update")
            lineas += [f"## {x['seccion']}. {d['titulo']}", ""] + cuerpo + [""]
    refs = _referencias([P.run_dir(s, r, pl["raiz"]) for s, r, _ in pl["corridas"]])
    lineas += ["# Referencias bibliográficas", ""]
    if refs:
        for r in refs:
            lineas += [r, ""]
    else:
        lineas += [f"{PENDIENTE}: ninguna de las corridas usadas aporta referencias.", ""]
    anexos_txt = {}
    if pl["anexos"]:
        lineas += ["# Anexos", ""]
        for a in pl["anexos"]:
            lugar = f"el anexo {a['anexo']}"
            cuerpo = _cuerpo(a["archivo"].read_text(encoding="utf-8"), a["anexo"], st.avisos, lugar)
            ctx = {"dir": a["dir"], "skill": a["skill"], "lugar": f"Anexo {a['anexo']}", "titulo": a["titulo"]}
            figs, tabs = st.figuras, st.tablas
            propio = _procesar(st, list(cuerpo), ctx, "../imagenes/", copiar=False)
            st.figuras, st.tablas = figs, tabs
            en_informe = _procesar(st, cuerpo, ctx)
            lineas += [f"## Anexo {a['anexo']}: {a['titulo']}", ""] + en_informe + [""]
            sube = [re.sub(r"^#(#+) ", r"\1 ", l) if RE_HEAD.match(l) else l for l in propio]
            anexos_txt[a["anexo"]] = "\n".join([f"# Anexo {a['anexo']}: {a['titulo']}", ""] + sube) + "\n"
    texto = _refs_figura("\n".join(lineas), st)
    anexos_txt = {k: _refs_figura(v, st) for k, v in anexos_txt.items()}
    texto = re.sub(r"\n{3,}", "\n\n", texto).rstrip("\n") + "\n"
    return texto, anexos_txt, st, portada, not refs


def construir(raiz=None, salida=None, curso=None, docente=None):
    if salida is None:
        raise ReportError("indica la carpeta de la corrida (--salida), creada con runs.py new --step 12-make-report")
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    if (salida / INFORME).exists():
        raise ReportError(f"{salida} ya tiene un informe: crea una corrida nueva con runs.py new --step {PASO}")
    pl = plan(raiz)
    texto, anexos_txt, st, portada, sin_refs = armar(pl, salida, curso, docente)
    (salida / INFORME).write_text(texto, encoding="utf-8")
    for letra, t in anexos_txt.items():
        (salida / "anexos").mkdir(exist_ok=True)
        (salida / "anexos" / f"anexo-{letra.lower()}.md").write_text(re.sub(r"\n{3,}", "\n\n", t), encoding="utf-8")
    escribir_indice_imagenes(st)
    (salida / "faltantes.md").write_text(escribir_faltantes(pl, st, portada, sin_refs), encoding="utf-8")
    (salida / "README.md").write_text(escribir_readme(pl, st, curso, docente, pl["anexos"]), encoding="utf-8")
    return {"informe": salida / INFORME, "incluidas": [x["seccion"] for x in pl["incluidas"]], "pendientes": [x["seccion"] for x in pl["pendientes"]],
            "anexos": [a["anexo"] for a in pl["anexos"]], "figuras": st.figuras, "tablas": st.tablas, "avisos": st.avisos, "portada": portada}


# ---------------------------------------------------------------- HTML
def tokens(raiz, cfg):
    """(tokens, usa_base): los del tokens.json junto al DESIGN.md del config o los base."""
    d = cfg.get("diseno")
    usa_base = not (d and (Path(raiz) / d).with_name("tokens.json").is_file())
    return DH.tokens_del_config(raiz, cfg), usa_base


def render(md_path, raiz=None):
    """Escribe informe.html junto al Markdown (autónomo, con el sistema de diseño). Devuelve (ruta, usa_base)."""
    raiz = P.repo_root(raiz)
    cfg = P.load(raiz)
    md_path = Path(md_path)
    tk, base = tokens(raiz, cfg)
    cuerpo, titulo = DH.md_a_html(md_path.read_text(encoding="utf-8"))
    titulo = titulo or f"Informe · {cfg['proyecto']['nombre']}"
    ruta = f'<nav class="ruta" aria-label="Ruta"><span aria-current="page">{html.escape(titulo)}</span></nav>'
    pagina = DH._pagina(DH._plantilla(), tk, titulo, ruta, cuerpo, "", f"{cfg['proyecto']['nombre']} · {md_path.name}", md_path.stem)
    out = md_path.with_suffix(".html")
    out.write_text(pagina, encoding="utf-8")
    return out, base


def anexos(raiz=None, run=None, comprobar=False):
    """HTML de los anexos de la corrida vigente (o `run`) de 12-make-report. Devuelve (carpeta, archivos o incidencias)."""
    raiz = P.repo_root(raiz)
    cfg = P.load(raiz)
    nombre = run or P.current_run(PASO, raiz)
    if not nombre:
        raise ReportError(f"no hay corrida vigente de {PASO}: ejecuta {PASO} primero")
    d = P.run_dir(PASO, nombre, raiz)
    if not d.is_dir():
        raise ReportError(f"no existe la corrida {d}")
    origen = d / "anexos"
    if not origen.is_dir() or not any(p for p in origen.glob("*.md")):
        raise ReportError(f"la corrida {nombre} no tiene anexos: salen de las secciones 3.1 (08-make-etl) y 3.2 (09-make-dashboard); "
                          "ejecútalas y vuelve a armar el informe")
    tk = DH.tokens_del_config(raiz, cfg)
    if comprobar:
        return d, DH.comprobar(origen, origen / "html", tk, NOMBRE_ANEXOS)
    return d, DH.construir(origen, origen / "html", tk, NOMBRE_ANEXOS)


# ---------------------------------------------------------------- CLI
def _plan_json(pl):
    limpio = lambda xs: [{k: (str(v) if isinstance(v, Path) else v) for k, v in x.items()} for x in xs]  # noqa: E731
    return {"incluidas": limpio(pl["incluidas"]), "pendientes": pl["pendientes"], "anexos": limpio(pl["anexos"]),
            "anexos_pendientes": pl["anexos_pendientes"], "figuras": pl["figuras"],
            "corridas": [{"skill": s, "run": r, "secciones": secs} for s, r, secs in pl["corridas"]], "brief": pl["brief"] is not None}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--json", action="store_true"); p.add_argument("--raiz")
    c = sub.add_parser("construir"); c.add_argument("--salida", required=True); c.add_argument("--curso"); c.add_argument("--docente"); c.add_argument("--raiz")
    r = sub.add_parser("render"); r.add_argument("informe"); r.add_argument("--raiz")
    a_ = sub.add_parser("anexos"); a_.add_argument("--run"); a_.add_argument("--comprobar", action="store_true"); a_.add_argument("--raiz")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "plan":
            pl = plan(a.raiz)
            if a.json:
                print(json.dumps(_plan_json(pl), ensure_ascii=False, indent=1))
                return 0
            total = len(pl["idx"]["puntos"])
            print(f"Secciones disponibles: {len(pl['incluidas'])} de {total}")
            for s, r_, secs in pl["corridas"]:
                print(f"  {s} ({r_}): {', '.join(secs)}")
            print("\nPendientes (van a faltantes.md):")
            for x in pl["pendientes"]:
                print(f"  {x['seccion']:>5}  {x['titulo']}  ·  {x['motivo']}")
            if not pl["pendientes"]:
                print("  (ninguna)")
            print("\nAnexos:")
            for x in pl["anexos"]:
                print(f"  {x['anexo']}  {x['titulo']}  ·  {x['skill']} ({x['run']})")
            for x in pl["anexos_pendientes"]:
                print(f"  {x['anexo']}  {x['titulo']}  ·  pendiente: {x['motivo']}")
            print("\nFiguras:")
            for f in pl["figuras"]:
                falta = [n for n, ok in (("HTML", f["html"]), ("explicación", f["explicacion"])) if not ok]
                print(f"  {f['lugar']}: {f['visual']}" + (f"  ·  falta {' y '.join(falta)} ({f['skill']}-update)" if falta else ""))
            if not pl["figuras"]:
                print("  (ninguna)")
            print("\nBrief vigente: " + ("sí" if pl["brief"] else "no (la empresa quedará «Pendiente»)"))
            return 0
        if a.cmd == "construir":
            res = construir(a.raiz, a.salida, a.curso, a.docente)
            print(f"Escrito {res['informe']} ({len(res['incluidas'])} secciones, {len(res['pendientes'])} pendientes, "
                  f"{len(res['anexos'])} anexos, {res['figuras']} figuras)")
            for av in res["avisos"]:
                print(f"AVISO: {av}")
            return 0
        if a.cmd == "render":
            out, base = render(a.informe, a.raiz)
            print(out)
            if base:
                print("AVISO: se usaron los tokens base porque el config no tiene sistema de diseño (02-design-system)")
            return 0
        d, res = anexos(a.raiz, a.run, a.comprobar)
        if a.comprobar:
            for f, causa in res:
                print(f"{f}: {causa}")
            print("sin incidencias" if not res else f"{len(res)} incidencia(s)")
            return 1 if res else 0
        print(f"{len(res)} archivos en {d / 'anexos' / 'html'}")
        return 0
    except (P.ConfigError, ReportError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
