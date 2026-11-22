#!/usr/bin/env python3
"""Visuales HTML del informe: extracción de sus datos desde el markdown de las corridas vigentes.

  python3 .claude/skills/_shared/visuales.py disponibles [--raiz .]
  python3 .claude/skills/_shared/visuales.py extraer --visual <visual> [--run CORRIDA] [--raiz .] [--salida datos.json]
  python3 .claude/skills/_shared/visuales.py construir --visual <visual> --run CORRIDA --carpeta <corrida>/visuales [--diseno tokens.json] [--raiz .]
   (sin --diseno usa el sistema de diseño vigente del config, o los tokens base si no hay)
  python3 .claude/skills/_shared/visuales.py origen --visual <visual>            (skill, archivo y -update que lo cambian)

El markdown de las skills de origen es la fuente de verdad: aquí solo se lee. Cada visual tiene su plantilla en
common/html/<plantilla>/. `construir` escribe <visual>.json y <visual>.html y, al lado de visuales/, leer-imagen/<visual>.md
(puntos cortos que explican qué muestra la imagen y qué transmite, para el informe).

Los registros (VISUALES, EXTRACTORES, EXPLICACION, PROPOSITOS, TITULOS y ORIGEN) los completa cada skill que aporta
un visual: hoy el Business Model Canvas (1.4), el PESTEL (1.5), el FODA (1.6) y el Ishikawa (1.7) del capítulo 1, la arquitectura de BI
(2.2) y el modelo de datos (2.4, desde `modelo.json`) del capítulo 2, que se leen de `secciones/<punto>.md` de la corrida indicada con --run (la nueva, antes de registrarla) o de la vigente.
Solo biblioteca estándar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import html_tpl as H  # noqa: E402
import projectcfg as P  # noqa: E402

# visual -> (plantilla, paso de origen o None, carpeta del paso)
VISUALES = {
    "bmc": ("bmc", "03-make-business-diagnosis", "03-business-diagnosis"),
    "pestel": ("pestel", "04-make-strategic-analysis", "04-strategic-analysis"),
    "foda": ("foda", "04-make-strategic-analysis", "04-strategic-analysis"),
    "ishikawa": ("ishikawa", "04-make-strategic-analysis", "04-strategic-analysis"),
    "arquitectura-bi": ("arquitectura-bi", "06-make-bi-solution", "06-bi-solution"),
    "modelo-datos": ("modelo-datos", "07-make-data-model-kpi", "07-data-model-kpi"),
}
PLANTILLAS = sorted({v[0] for v in VISUALES.values()})


class SinFuente(Exception):
    """Falta la corrida o el archivo de origen de un visual."""


# ------------------------------------------------------------------ lectura de markdown
def _limpia(s):
    return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "")).strip()


def tablas(txt):
    """Todas las tablas de un markdown: lista de (encabezados, filas) con las celdas como texto."""
    out, cur = [], []
    for ln in txt.splitlines() + [""]:
        if ln.strip().startswith("|"):
            cur.append(ln.strip())
            continue
        if len(cur) >= 2:
            filas = [[_limpia(c) for c in r.strip("|").split("|")] for r in cur]
            if all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cur[1].strip("|").split("|")):
                out.append((filas[0], filas[2:]))
        cur = []
    return out


def _norm(s):
    return re.sub(r"[^a-z0-9 ]", "", _sin_tildes(s).lower()).strip()


def _busca(enc, nombre):
    """Índice de la columna `nombre`: por coincidencia completa o, si no, por las 3 primeras letras (Imp. = Impacto)."""
    n = _norm(nombre)
    e = [_norm(x) for x in enc]
    for i, x in enumerate(e):
        if n in x:
            return i
    for i, x in enumerate(e):
        if len(n) > 3 and n[:3] in x.split(" ")[0][:3]:
            return i
    return None


def tabla(txt, *claves):
    """Primera tabla cuyo encabezado tiene todas las `claves` (sin tildes ni mayúsculas); None si no hay."""
    for enc, filas in tablas(txt):
        if all(_busca(enc, c) is not None for c in claves):
            return enc, filas
    return None


def _sin_tildes(s):
    return s.translate(str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU"))


def secciones(txt, nivel=2):
    """{título: cuerpo} de los encabezados del nivel indicado."""
    partes = re.split(rf"(?m)^{'#' * nivel}\s+(?!#)(.+)$", txt)
    return {partes[i].strip(): partes[i + 1].strip() for i in range(1, len(partes) - 1, 2)}


def campo(txt, rotulo):
    """Valor de «**Rótulo.** valor» (hasta el siguiente rótulo o el fin de la línea/párrafo)."""
    m = re.search(rf"\*\*{re.escape(rotulo)}[.:]?\*\*\s*(.*?)(?=\s*\*\*[^*]+\*\*|\n\s*\n|\Z)", txt, re.S)
    return _limpia(m.group(1)) if m else ""


def fecha_iso(s):
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})", s or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def _entero(s):
    m = re.search(r"[−-]?\d+", (s or "").replace("−", "-"))
    return int(m.group(0)) if m else 0


def _item(celda):
    """«texto» (REF) -> {texto, ref}."""
    c = _limpia(celda)
    m = re.match(r"^(.*?)\s*\(([^()]*)\)\.?$", c)
    texto, ref = (m.group(1), m.group(2)) if m else (c, "")
    ref = re.sub(r"^(?:inferid[oa]s? de|basad[oa]s? en)\s+", "", ref.strip(), flags=re.I)
    return {"texto": texto.strip().strip("«»\"“” ").rstrip(".;").strip(), "ref": ref.strip()}


def _col(enc, fila, *nombres):
    for nom in nombres:
        i = _busca(enc, nom)
        if i is not None and i < len(fila):
            return fila[i]
    return ""


# ------------------------------------------------------------------ corridas vigentes
def _run(raiz, paso, carpeta):
    try:
        r = P.current_run(paso, raiz)
    except P.ConfigError as e:
        raise SinFuente(str(e))
    if not r:
        raise SinFuente(f"no hay una corrida vigente de {paso}")
    return Path(raiz) / "project" / carpeta / r


def _leer(run, *nombres):
    """Primer archivo de la corrida con alguno de esos nombres (en cualquier subcarpeta)."""
    for nom in nombres:
        f = run / nom
        if not f.exists():
            hallados = sorted(run.rglob(nom))
            f = hallados[0] if hallados else None
        if f is not None and f.exists():
            return f.read_text(encoding="utf-8")
    raise SinFuente(f"falta {' o '.join(nombres)} en la corrida {run.name}")


def proyecto(raiz):
    try:
        p = P.load(raiz)["proyecto"]
        return p["nombre"] if isinstance(p, dict) else str(p)
    except (P.ConfigError, KeyError, OSError):
        return ""


def _base(raiz):
    return {"schema": 1, "proyecto": proyecto(raiz)}


# ------------------------------------------------------------------ extractores (capítulo 1)
def _diag(visual, raiz, run, lector):
    """Datos de la corrida `run` (o la vigente) del paso de origen del visual, leídos con diagnostico.<lector>."""
    import diagnostico as D
    try:
        return getattr(D, lector)(D.corrida(raiz, VISUALES[visual][1], run))
    except D.SinCorrida as e:
        raise SinFuente(str(e))


def ex_bmc(raiz, run=None, **_):
    import diagnostico as D
    d = _diag("bmc", raiz, run, "leer_negocio")
    por = {D.norm(b["bloque"]): b["items"] for b in d["canvas"]}
    if not any(por.values()):
        raise SinFuente("secciones/1.4.md no tiene la tabla «Bloque | Contenido» del Business Model Canvas")
    claves = ["segmentos", "propuesta", "canales", "relaciones", "ingresos", "recursos", "actividades", "socios", "costos"]
    bloques = [{"clave": c, "nombre": n, "items": [i[:1].upper() + i[1:] for i in por.get(D.norm(n), [])]}
               for c, n in zip(claves, D.BLOQUES_BMC)]
    return {**_base(raiz), "empresa": d["empresa"].get("Nombre comercial", ""), "bloques": bloques}


def ex_pestel(raiz, run=None, **_):
    import diagnostico as D
    d = _diag("pestel", raiz, run, "leer_estrategico")
    if not d["pestel"]:
        raise SinFuente("secciones/1.5.md no tiene la tabla «Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente»")
    claves = {"POL": "politico", "ECO": "economico", "SOC": "social", "TEC": "tecnologico", "AMB": "ecologico", "LEG": "legal"}
    factores = []
    for pref, nombre in D.FACTORES.items():
        items = [{"codigo": i["codigo"], "texto": i["hallazgo"], "efecto": i["efecto"], "tipo": i["tipo"], "fuente": i["fuente"]}
                 for i in d["pestel"] if i["codigo"].startswith(pref + "-")]
        factores.append({"clave": claves[pref], "nombre": nombre, "items": items})
    return {**_base(raiz), "factores": factores}


def ex_foda(raiz, run=None, **_):
    d = _diag("foda", raiz, run, "leer_estrategico")
    if not any(d["foda"].values()):
        raise SinFuente("secciones/1.6.md no tiene los ítems FOR, DEB, OPO y AME del FODA")
    estrategias = [{"codigo": e["codigo"], "tipo": e["tipo"], "texto": e["texto"], "combina": e["combina"]} for e in d["estrategias"]]
    return {**_base(raiz), "cuadrantes": d["foda"], "estrategias": estrategias}


def ex_ishikawa(raiz, run=None, **_):
    import diagnostico as D
    d = _diag("ishikawa", raiz, run, "leer_estrategico")
    if not d["causas"]:
        raise SinFuente("secciones/1.7.md no tiene la tabla «Código | Categoría | Causa | Evidencia» del Ishikawa")
    cats = []
    for c in D.CATEGORIAS_6M + sorted({x["categoria"] for x in d["causas"]} - set(D.CATEGORIAS_6M)):
        causas = [{"codigo": x["codigo"], "texto": x["causa"]} for x in d["causas"] if x["categoria"] == c]
        if causas:
            cats.append({"nombre": c, "causas": causas})
    return {**_base(raiz), "efecto": d["efecto"].rstrip("."), "categorias": cats}


def ex_arquitectura(raiz, run=None, **_):
    import diagnostico as D
    d = _diag("arquitectura-bi", raiz, run, "leer_solucion")
    if not d["componentes"]:
        raise SinFuente("secciones/2.2.md no tiene la tabla «Código | Capa | Componente | Función | Entrada y salida»")
    capas = []
    for clave, nombre in zip(D.CLAVES_CAPA, D.CAPAS):
        comps = [{"codigo": c["codigo"], "nombre": c["componente"], "funcion": c["funcion"], "entrada_salida": c["entrada_salida"]}
                 for c in d["componentes"] if D.norm(c["capa"]) == D.norm(nombre)]
        herr = [h["herramienta"] for h in d["herramientas"] if D.norm(h["capa"]) == D.norm(nombre) and h["herramienta"]]
        capas.append({"clave": clave, "nombre": nombre, "herramientas": herr, "componentes": comps})
    return {**_base(raiz), "capas": capas}


def ex_modelo(raiz, run=None, **_):
    d = _diag("modelo-datos", raiz, run, "leer_modelo")
    j = d["json"]
    if not j or not j.get("hechos") or not j.get("dimensiones"):
        raise SinFuente("falta modelo.json con hechos y dimensiones en la corrida (lo escribe 07-make-data-model-kpi junto a las secciones)")
    hechos = [{"codigo": h["codigo"], "nombre": h["nombre"], "granularidad": h["granularidad"],
               "medidas": [{"nombre": m["nombre"], "agregacion": m.get("agregacion", "")} for m in h.get("medidas", [])], "claves": h.get("claves", [])}
              for h in j["hechos"]]
    dims = [{"codigo": x["codigo"], "nombre": x["nombre"], "clave": x["clave"], "atributos": x.get("atributos", []), "jerarquias": x.get("jerarquias", [])}
            for x in j["dimensiones"]]
    rels = [{"codigo": r["codigo"], "desde": r["desde"], "hacia": r["hacia"], "campos": r["campos"], "cardinalidad": r["cardinalidad"],
             "filtro": r["filtro"]} for r in j.get("relaciones", [])]
    return {**_base(raiz), "hechos": hechos, "dimensiones": dims, "relaciones": rels}


# ------------------------------------------------------------------ registro de visuales
EXTRACTORES = {"bmc": ex_bmc, "pestel": ex_pestel, "foda": ex_foda, "ishikawa": ex_ishikawa,
               "arquitectura-bi": ex_arquitectura, "modelo-datos": ex_modelo}


def extraer(visual, raiz, run=None):
    """Datos del visual desde las corridas vigentes. Lanza SinFuente si falta algo."""
    if visual not in EXTRACTORES:
        raise SinFuente(f"visual desconocido: {visual} (hay: {', '.join(sorted(EXTRACTORES)) or 'ninguno'})")
    return EXTRACTORES[visual](raiz, run=run)


def disponibles(raiz, run=None):
    """{visual: None si hay fuente, o el motivo si falta}."""
    out = {}
    for v in sorted(EXTRACTORES):
        try:
            extraer(v, raiz, run)
            out[v] = None
        except SinFuente as e:
            out[v] = str(e)
    return out


# ------------------------------------------------------------------ «leer la imagen»
TITULOS = {"bmc": "Business Model Canvas", "pestel": "Análisis PESTEL", "foda": "Matriz FODA", "ishikawa": "Diagrama de Ishikawa",
           "arquitectura-bi": "Arquitectura de BI", "modelo-datos": "Modelo de datos en estrella"}
# Una frase fija por visual (para qué sirve la imagen); lo demás se deriva de los datos.
PROPOSITOS = {
    "bmc": "Muestra en una sola vista cómo la empresa crea, entrega y captura valor.",
    "pestel": "Resume los factores del entorno que favorecen o amenazan al negocio.",
    "foda": "Resume la situación de la empresa para decidir qué aprovechar y qué proteger.",
    "ishikawa": "Ordena por categorías las causas que explican el problema central del negocio.",
    "arquitectura-bi": "Muestra cómo viaja el dato desde las fuentes hasta el dashboard en cuatro capas.",
    "modelo-datos": "Muestra las tablas de hechos, las dimensiones y las relaciones sobre las que se calculan los indicadores.",
}

def _lista(items, n=3):
    items = [str(i) for i in items if i]
    if len(items) <= n:
        return ", ".join(items[:-1]) + (" y " if len(items) > 1 else "") + items[-1] if items else ""
    return ", ".join(items[:n]) + f" y {len(items) - n} más"


def _corto(t, n=110):
    t = str(t).strip().rstrip(".")
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _comp(a, b, x, y):
    return f"más {x} que {y}" if a > b else f"menos {x} que {y}" if a < b else f"tantas {x} como {y}"


def _pl(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


def _fecha_txt(d):
    return f"al {d[8:10]}-{d[5:7]}-{d[:4]}" if d else "Línea base"


# Purpose catalog: one fixed sentence per visual (what the image is for). Everything else is derived from the data.


ROTULO_SIRVE, ROTULO_DICE, ROTULO_RESALTA, ROTULO_PIE = "Para qué sirve", "Qué dice", "Por qué se resalta", "Pie de foto sugerido"
MAX_FRASES = 3
MAX_PALABRAS = 70


class SinProposito(KeyError):
    """The visual has no entry in PROPOSITOS."""


def armar_leer(titulo, sirve, dice, resalta, pie):
    """Text of a `leer-imagen/*.md` file: purpose, conclusion, optional reason for the highlight, and the suggested caption."""
    puntos = [(ROTULO_SIRVE, sirve), (ROTULO_DICE, dice)]
    if resalta:
        puntos.append((ROTULO_RESALTA, resalta))
    puntos.append((ROTULO_PIE, pie))
    return f"# Leer la imagen · {titulo}\n\n" + "\n".join(f"- **{r}.** {t}" for r, t in puntos) + "\n"


def _frases(texto):
    return len(re.findall(r"[.!?](?=\s+[A-ZÁÉÍÓÚÑ¿¡«0-9]|\s*$)", texto.strip()))


def validar_explicacion(texto, resaltado):
    """Causes (empty when valid) for a `leer-imagen` text: labels, highlight reason iff `resaltado`, sentence and word caps."""
    pts = {}
    for l in texto.splitlines():
        m = re.match(r"^- \*\*([^*]+?)\.\*\*\s*(.*)$", l)
        if m:
            pts[m.group(1)] = m.group(2).strip()
    causas = []
    for r in (ROTULO_SIRVE, ROTULO_DICE):
        if not pts.get(r):
            causas.append(f"falta la función «{r.lower()}»")
    if resaltado and not pts.get(ROTULO_RESALTA):
        causas.append("la imagen resalta algo y falta «por qué se resalta»")
    if not resaltado and ROTULO_RESALTA in pts:
        causas.append("incluye «por qué se resalta» pero la imagen no resalta nada")
    cuerpo = [pts[r] for r in (ROTULO_SIRVE, ROTULO_DICE, ROTULO_RESALTA) if pts.get(r)]
    if sum(_frases(t) for t in cuerpo) > MAX_FRASES or any(_frases(t) > 1 for t in cuerpo):
        causas.append(f"pasa de {MAX_FRASES} frases (una por función)")
    if sum(len(t.split()) for t in cuerpo) > MAX_PALABRAS:
        causas.append(f"pasa de {MAX_PALABRAS} palabras")
    if not pts.get(ROTULO_PIE):
        causas.append("falta el pie de foto sugerido")
    return causas

def _x_bmc(d):
    n = {b["clave"]: len(b["items"]) for b in d["bloques"]}
    return (f"El modelo atiende {_pl(n.get('segmentos', 0), 'segmento de clientes', 'segmentos de clientes')} por "
            f"{_pl(n.get('canales', 0), 'canal', 'canales')} y sostiene {_pl(n.get('ingresos', 0), 'fuente de ingresos', 'fuentes de ingresos')} "
            f"frente a {_pl(n.get('costos', 0), 'partida de costos', 'partidas de costos')}."), None


def _x_pestel(d):
    items = [i for f in d["factores"] for i in f["items"]]
    o = sum(1 for i in items if i.get("tipo") == "Oportunidad")
    a = sum(1 for i in items if i.get("tipo") == "Amenaza")
    am = {f["nombre"].lower(): sum(1 for i in f["items"] if i.get("tipo") == "Amenaza") for f in d["factores"]}
    tope = max(am.values(), default=0)
    mas = [n for n, k in am.items() if k == tope]
    cola = f", y las amenazas se concentran en el factor {mas[0]}" if tope > 1 and len(mas) == 1 else ""
    return f"De {_pl(len(items), 'hallazgo', 'hallazgos')} del entorno, {o} son oportunidades y {a} son amenazas{cola}.", None


def _x_foda(d):
    c = d["cuadrantes"]
    f, de, o, a = (len(c[k]) for k in ("fortalezas", "debilidades", "oportunidades", "amenazas"))
    dentro = "pesan más las fortalezas" if f > de else "pesan más las debilidades" if f < de else "fortalezas y debilidades se equilibran"
    fuera = "las oportunidades superan a las amenazas" if o > a else "las amenazas superan a las oportunidades" if o < a else "oportunidades y amenazas se equilibran"
    est = len(d.get("estrategias") or [])
    cola = f", y de su cruce salen {_pl(est, 'estrategia', 'estrategias')}" if est else ""
    return f"Por dentro {dentro} ({f} frente a {de}) y por fuera {fuera} ({o} frente a {a}){cola}.", None


def _x_ishikawa(d):
    cats = d["categorias"]
    total = sum(len(c["causas"]) for c in cats)
    tope = max((len(c["causas"]) for c in cats), default=0)
    mas = [c["nombre"].lower() for c in cats if len(c["causas"]) == tope]
    cola = f", con más peso en {_lista(mas)} ({_pl(tope, 'causa', 'causas')}{' cada una' if len(mas) > 1 else ''})" if tope > 1 and len(mas) < len(cats) else ""
    return (f"El problema «{_corto(d.get('efecto', ''), 90)}» se explica por {_pl(total, 'causa', 'causas')} "
            f"en {_pl(len(cats), 'categoría', 'categorías')}{cola}."), None


def _x_arquitectura(d):
    capas = {c["clave"]: c for c in d["capas"]}
    n = lambda k: len(capas.get(k, {}).get("componentes", []))
    herr = [h for c in d["capas"] for h in c["herramientas"]]
    pend = sum(1 for h in herr if h.strip().rstrip(".").lower() == "pendiente")
    cola = f", y {_pl(pend, 'herramienta está pendiente', 'herramientas están pendientes')} de decidir" if pend else ""
    return (f"Los datos pasan de {_pl(n('fuentes'), 'fuente', 'fuentes')} por {_pl(n('etl'), 'componente', 'componentes')} de ETL y "
            f"{_pl(n('almacenamiento'), 'de almacenamiento', 'de almacenamiento')} hasta {_pl(n('visualizacion'), 'componente', 'componentes')} de visualización{cola}."), None


def _x_modelo(d):
    h, x, r = len(d["hechos"]), len(d["dimensiones"]), len(d["relaciones"])
    tope = max(d["hechos"], key=lambda f: len(f["claves"]), default=None)
    cola = f", y {tope['nombre']} es el hecho con más ejes de análisis ({_pl(len(tope['claves']), 'clave', 'claves')})" if tope and len(d["hechos"]) > 1 else ""
    return (f"El modelo tiene {_pl(h, 'tabla de hechos', 'tablas de hechos')} y {_pl(x, 'dimensión', 'dimensiones')} unidas por "
            f"{_pl(r, 'relación', 'relaciones')}{cola}."), None


# visual -> función(datos) que devuelve (qué dice, por qué se resalta o None)
EXPLICACION = {"bmc": _x_bmc, "pestel": _x_pestel, "foda": _x_foda, "ishikawa": _x_ishikawa,
               "arquitectura-bi": _x_arquitectura, "modelo-datos": _x_modelo}


def resaltado(visual, datos):
    """True cuando los datos de la imagen resaltan algo (y su explicación debe decir por qué)."""
    return EXPLICACION[visual](datos)[1] is not None


def leer_imagen(visual, datos):
    """Texto de `leer-imagen/<visual>.md`: para qué sirve la imagen, qué dice y por qué resalta algo, derivado de los datos."""
    if visual not in PROPOSITOS:
        raise SinProposito(visual)
    dice, resalta = EXPLICACION[visual](datos)
    return armar_leer(TITULOS[visual], PROPOSITOS[visual], dice, resalta, f"Figura X: {TITULOS[visual]}.")


# visual -> (skill de origen, archivo de la corrida)
ORIGEN = {
    "bmc": ("03-make-business-diagnosis", "secciones/1.4.md"),
    "pestel": ("04-make-strategic-analysis", "secciones/1.5.md"),
    "foda": ("04-make-strategic-analysis", "secciones/1.6.md"),
    "ishikawa": ("04-make-strategic-analysis", "secciones/1.7.md"),
    "arquitectura-bi": ("06-make-bi-solution", "secciones/2.2.md"),
    "modelo-datos": ("07-make-data-model-kpi", "secciones/2.4.md"),
}


def origen(visual):
    """(skill de origen, archivo, skill -update que lo modifica); None si el visual no está registrado."""
    if visual not in ORIGEN:
        return None
    paso, archivo = ORIGEN[visual]
    return paso, archivo, f"{paso}-update"


def construir(visual, raiz, carpeta, tokens, run=None):
    """Escribe <carpeta>/<visual>.json y <carpeta>/<visual>.html; devuelve los datos."""
    datos = extraer(visual, raiz, run)
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{visual}.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / f"{visual}.html").write_text(H.copiar_texto(VISUALES[visual][0], datos, tokens), encoding="utf-8")
    leer = carpeta.parent / "leer-imagen"
    leer.mkdir(exist_ok=True)
    (leer / f"{visual}.md").write_text(leer_imagen(visual, datos), encoding="utf-8")
    return datos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("disponibles", "extraer", "construir", "origen"):
        s = sub.add_parser(n)
        s.add_argument("--raiz", default=".")
        s.add_argument("--run")
        if n in ("extraer", "construir", "origen"):
            s.add_argument("--visual", required=True)
        if n == "extraer":
            s.add_argument("--salida")
        if n == "construir":
            s.add_argument("--carpeta", required=True)
            s.add_argument("--diseno")
    a = ap.parse_args(argv)
    raiz = Path(a.raiz).resolve()
    try:
        if a.cmd == "disponibles":
            for v, motivo in disponibles(raiz, a.run).items():
                print(f"{v}: {'disponible' if motivo is None else 'falta fuente — ' + motivo}")
            return 0
        if a.cmd == "origen":
            o = origen(a.visual)
            print("visual no registrado" if o is None else f"{o[0]} · {o[1]} · se cambia con {o[2]}")
            return 0
        if a.cmd == "extraer":
            txt = json.dumps(extraer(a.visual, raiz, a.run), ensure_ascii=False, indent=2) + "\n"
            if a.salida:
                Path(a.salida).write_text(txt, encoding="utf-8")
            else:
                print(txt, end="")
            return 0
        tokens = H.cargar_tokens(raiz, a.diseno) if a.diseno else H.tokens_del_proyecto(raiz)
        construir(a.visual, raiz, a.carpeta, tokens, a.run)
        print(Path(a.carpeta) / f"{a.visual}.html")
        return 0
    except SinFuente as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
