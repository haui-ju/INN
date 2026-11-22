#!/usr/bin/env python3
"""Capítulos 1 y 2 del informe (diagnóstico estratégico y diseño de la solución): lectura de las secciones de las corridas y comprobaciones comunes.

  python3 .claude/skills/_shared/diagnostico.py leer --paso 04-make-strategic-analysis [--run CORRIDA] [--raiz .]
  python3 .claude/skills/_shared/diagnostico.py titulos                       (encabezado exacto de cada punto del índice)

Cada skill de los capítulos 1 y 2 escribe en su corrida `secciones/<punto>.md` (encabezado `## <punto>. <título del índice>`),
marca sus figuras con `<!-- figura: <visual> -->`, deja el HTML en `visuales/`, su explicación en `leer-imagen/` y,
si cita, `referencias.md` (APA 7). Este módulo lee esas secciones como datos (tablas y rótulos) para los validadores,
los visuales y las skills siguientes, y ofrece las comprobaciones que comparten los pasos. Solo biblioteca estándar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import projectcfg as P  # noqa: E402
import visuales as VI  # noqa: E402

INDICE = HERE.parents[2] / "common" / "structure" / "model1.md"
NEGOCIO, ESTRATEGICO, PROBLEMA = "03-make-business-diagnosis", "04-make-strategic-analysis", "05-make-problem-objectives"
SOLUCION, MODELO = "06-make-bi-solution", "07-make-data-model-kpi"
FIGURAS = {"1.4": ["bmc"], "1.5": ["pestel"], "1.6": ["foda"], "1.7": ["ishikawa"], "2.2": ["arquitectura-bi"], "2.4": ["modelo-datos"]}
RE_FIGURA = re.compile(r"^<!-- figura: ([a-z0-9-]+) -->$")
MARCADOR = re.compile(r"\((?:modelado por el agente|fuente:)[^)]*\)", re.I)
PENDIENTE = "Pendiente"

BLOQUES_BMC = ["Segmentos de clientes", "Propuesta de valor", "Canales", "Relaciones con clientes", "Fuentes de ingresos",
               "Recursos clave", "Actividades clave", "Socios clave", "Estructura de costos"]
FACTORES = {"POL": "Político", "ECO": "Económico", "SOC": "Social", "TEC": "Tecnológico", "AMB": "Ecológico", "LEG": "Legal"}
CUADRANTES = {"FOR": "fortalezas", "DEB": "debilidades", "OPO": "oportunidades", "AME": "amenazas"}
NOMBRE_CUADRANTE = {"FOR": "Fortaleza", "DEB": "Debilidad", "OPO": "Oportunidad", "AME": "Amenaza"}
ESTRATEGIAS = {"FO": ("FOR", "OPO"), "FA": ("FOR", "AME"), "DO": ("DEB", "OPO"), "DA": ("DEB", "AME")}
CATEGORIAS_6M = ["Método", "Mano de obra", "Materiales", "Maquinaria", "Medición", "Medio ambiente"]
TIPOS_PESTEL = ("Oportunidad", "Amenaza")
RE_PESTEL = re.compile(r"\b(?:POL|ECO|SOC|TEC|AMB|LEG)-\d+\b")
RE_FODA = re.compile(r"\b(?:FOR|DEB|OPO|AME)-\d+\b")
RE_EST = re.compile(r"\b(?:FO|FA|DO|DA)-\d+\b")
RE_CAU = re.compile(r"\bCAU-\d+\b")
RE_CAP = re.compile(r"\bCAP-\d+\b")
RE_FUE = re.compile(r"\bFUE-\d+\b")
CAPAS = ["Fuentes", "ETL", "Almacenamiento", "Visualización"]
CLAVES_CAPA = ["fuentes", "etl", "almacenamiento", "visualizacion"]
AGREGACIONES = ("suma", "promedio", "conteo", "conteo distinto", "mínimo", "máximo")
CARDINALIDADES = ("*:1", "1:*", "1:1", "*:*")
FILTROS = ("Simple", "Ambos")
FRECUENCIAS = ("Diaria", "Semanal", "Mensual", "Trimestral", "Anual", "Por carga")
PERIODICAS = ("diaria", "semanal", "mensual", "trimestral", "anual")


class SinCorrida(Exception):
    """Falta la corrida o una sección de un paso del capítulo 1."""


# ------------------------------------------------------------------ índice y encabezados
def titulos():
    """{punto: título exacto} del índice: el texto del punto sin los paréntesis finales."""
    out = {}
    for ln in INDICE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- (\d+(?:\.\d+)?)\. (.+)$", ln)
        if m:
            t = m.group(2).strip()
            while True:
                n = re.sub(r"\s*\([^()]*\)\s*$", "", t)
                if n == t:
                    break
                t = n
            out[m.group(1)] = t
    return out


def encabezado(punto):
    return f"## {punto}. {titulos()[punto]}"


def puntos_de(paso):
    return list(P.step_info(paso)["secciones"])


def corrida(raiz, paso, run=None):
    """Carpeta de la corrida `run` (o la vigente) del paso; lanza SinCorrida si no hay."""
    carpeta = P.step_info(paso)["carpeta"]
    if run is None:
        try:
            run = P.current_run(paso, raiz)
        except P.ConfigError as e:
            raise SinCorrida(str(e))
    if not run:
        raise SinCorrida(f"no hay una corrida vigente de {paso}")
    d = Path(run) if Path(run).is_absolute() else Path(raiz) / "project" / carpeta / run
    if not d.is_dir():
        raise SinCorrida(f"no existe la corrida {d.name} de {paso}")
    return d


def texto(run, punto):
    """Texto de `secciones/<punto>.md` o None."""
    f = Path(run) / "secciones" / f"{punto}.md"
    return f.read_text(encoding="utf-8") if f.is_file() else None


def _seccion(run, punto):
    t = texto(run, punto)
    if t is None:
        raise SinCorrida(f"falta secciones/{punto}.md en la corrida {Path(run).name}")
    return t


# ------------------------------------------------------------------ utilidades de lectura
def norm(t):
    """Texto comparable: sin marcadores, comillas, espacios repetidos ni punto final."""
    t = MARCADOR.sub("", t or "").replace("**", "")
    t = re.sub(r"\s+", " ", t).strip().strip("«»\"“”").strip()
    return t.rstrip(".").strip().lower()


def pendiente(t):
    return (t or "").strip().rstrip(".").lower() == PENDIENTE.lower()


def numero(t):
    """Primer número de un texto («S/ 2 400 000 (2025)» -> 2400000.0; «436,4» -> 436.4); None si no hay."""
    m = re.search(r"\d{1,3}(?:[  .,]\d{3})+(?:,\d+)?(?!\d)|\d+(?:[.,]\d+)?", t or "")
    if not m:
        return None
    s = m.group(0).replace(" ", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", s):
        s = s.replace(",", "")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def vinetas(txt, rotulo):
    m = re.search(r"\*\*" + re.escape(rotulo) + r"\.?\*\*\s*\n((?:\s*- .+\n?)+)", txt + "\n")
    return [re.sub(r"\s+", " ", x.strip()[2:]).strip() for x in m.group(1).strip().splitlines()] if m else []


def _filas(txt, *claves):
    t = VI.tabla(txt, *claves)
    return (t[0], t[1]) if t else (None, [])


def _codigos(t, rx):
    return rx.findall(t or "")


def _items(celda):
    return [x.strip().rstrip(".") for x in re.split(r";", celda or "") if x.strip()]


# ------------------------------------------------------------------ lectura por paso
def leer_negocio(run):
    """Datos de 1.1 a 1.4 de una corrida de 03-make-business-diagnosis."""
    s11, s12, s13, s14 = (_seccion(run, p) for p in ("1.1", "1.2", "1.3", "1.4"))
    enc, filas = _filas(s11, "Dato", "Valor")
    empresa = {f[0]: f[1] for f in filas if len(f) >= 2}
    ia_enc, ia = _filas(s13, "Aspecto", "Descripcion")
    ta_enc, ta = _filas(s13, "Dato", "Valor")
    bm_enc, bm = _filas(s14, "Bloque", "Contenido")
    canvas = [{"bloque": f[0], "items": _items(VI._col(bm_enc, f, "Contenido"))} for f in bm if f and f[0]]
    return {
        "empresa": empresa, "resena": VI.campo(s11, "Reseña"),
        "mision": VI.campo(s12, "Misión"), "vision": VI.campo(s12, "Visión"), "valores": vinetas(s12, "Valores"),
        "relacion": VI.campo(s12, "Relación con el proyecto"),
        "industria": {f[0]: f[1] for f in ia if len(f) >= 2}, "tamano": {f[0]: f[1] for f in ta if len(f) >= 2},
        "canvas": canvas, "lectura": VI.campo(s14, "Lectura del modelo"),
    }


def leer_estrategico(run):
    """Datos de 1.5 a 1.7 de una corrida de 04-make-strategic-analysis."""
    s15, s16, s17 = (_seccion(run, p) for p in ("1.5", "1.6", "1.7"))
    pe_enc, pe = _filas(s15, "Codigo", "Factor", "Hallazgo")
    pestel = [{"codigo": f[0], "factor": VI._col(pe_enc, f, "Factor"), "hallazgo": VI._col(pe_enc, f, "Hallazgo"),
               "efecto": VI._col(pe_enc, f, "Efecto"), "tipo": VI._col(pe_enc, f, "Tipo"), "fuente": VI._col(pe_enc, f, "Fuente")}
              for f in pe if f and RE_PESTEL.fullmatch(f[0])]
    foda = {v: [] for v in CUADRANTES.values()}
    for pref, clave in CUADRANTES.items():
        enc, filas = _filas(s16, "Codigo", NOMBRE_CUADRANTE[pref])
        foda[clave] = [{"codigo": f[0], "texto": VI._col(enc, f, NOMBRE_CUADRANTE[pref]), "evidencia": VI._col(enc, f, "Evidencia")}
                       for f in filas if f and re.fullmatch(rf"{pref}-\d+", f[0])]
    es_enc, es = _filas(s16, "Codigo", "Tipo", "Estrategia", "Combina")
    estrategias = [{"codigo": f[0], "tipo": VI._col(es_enc, f, "Tipo"), "texto": VI._col(es_enc, f, "Estrategia"),
                    "combina": _codigos(VI._col(es_enc, f, "Combina"), RE_FODA)} for f in es if f and RE_EST.fullmatch(f[0])]
    ca_enc, ca = _filas(s17, "Codigo", "Categoria", "Causa")
    causas = [{"codigo": f[0], "categoria": VI._col(ca_enc, f, "Categoria"), "causa": VI._col(ca_enc, f, "Causa"),
               "evidencia": VI._col(ca_enc, f, "Evidencia")} for f in ca if f and RE_CAU.fullmatch(f[0])]
    return {"pestel": pestel, "foda": foda, "estrategias": estrategias, "efecto": VI.campo(s17, "Efecto"), "causas": causas}


def leer_problema(run):
    """Datos de 1.8 a 1.10 de una corrida de 05-make-problem-objectives."""
    import brief as BR
    s18, s19, s110 = (_seccion(run, p) for p in ("1.8", "1.9", "1.10"))
    pr_enc, pr = _filas(s18, "Codigo", "Causa")
    principales = [{"codigo": f[0], "causa": VI._col(pr_enc, f, "Causa"), "categoria": VI._col(pr_enc, f, "Categoria"),
                    "evidencia": VI._col(pr_enc, f, "Evidencia")} for f in pr if f and RE_CAU.fullmatch(f[0])]
    ma_enc, ma = _filas(s110, "Objetivo", "Causas", "Canvas")
    matriz = []
    for f in ma:
        if not f or not re.fullmatch(r"O[GE]-\d+", f[0]):
            continue
        canvas = VI._col(ma_enc, f, "Canvas")
        matriz.append({"objetivo": f[0], "causas": _codigos(VI._col(ma_enc, f, "Causas"), RE_CAU),
                       "foda": _codigos(VI._col(ma_enc, f, "FODA"), RE_FODA) + _codigos(VI._col(ma_enc, f, "FODA"), RE_EST),
                       "pestel_txt": VI._col(ma_enc, f, "PESTEL"), "pestel": _codigos(VI._col(ma_enc, f, "PESTEL"), RE_PESTEL),
                       "canvas": [x.strip().rstrip(".") for x in re.split(r"[;,]", canvas) if x.strip()],
                       "indicador": VI._col(ma_enc, f, "Indicador")})
    return {"enunciado": VI.campo(s18, "Enunciado"), "afectados": VI.campo(s18, "Afectados"), "principales": principales,
            "evidencia": vinetas(s18, "Evidencia"), "og": BR._objetivos(s19), "oe": BR._objetivos(s110), "matriz": matriz}


def _partes(celda):
    """«a; b; c» -> ['a', 'b', 'c'] (sin vacíos ni «—»)."""
    return [x.strip().rstrip(".") for x in re.split(r";", celda or "") if x.strip() and x.strip() not in ("—", "-", "–")]


def _medidas(celda):
    out = []
    for x in _partes(celda):
        m = re.match(r"^(.+?)\s*\(([^()]*)\)$", x)
        out.append({"nombre": (m.group(1) if m else x).strip(), "agregacion": (m.group(2) if m else "").strip()})
    return out


def leer_solucion(run):
    """Datos de 2.1 a 2.3 de una corrida de 06-make-bi-solution."""
    s21, s22, s23 = (_seccion(run, p) for p in ("2.1", "2.2", "2.3"))
    ob_enc, ob = _filas(s21, "Objetivo", "Componentes")
    objetivos = [{"objetivo": f[0], "componentes": _codigos(VI._col(ob_enc, f, "Componentes"), RE_CAP), "como": VI._col(ob_enc, f, "Como lo atiende")}
                 for f in ob if f and re.fullmatch(r"OE-\d+", f[0])]
    co_enc, co = _filas(s22, "Codigo", "Capa", "Componente")
    componentes = [{"codigo": f[0], "capa": VI._col(co_enc, f, "Capa"), "componente": VI._col(co_enc, f, "Componente"),
                    "funcion": VI._col(co_enc, f, "Funcion"), "entrada_salida": VI._col(co_enc, f, "Entrada")}
                   for f in co if f and RE_CAP.fullmatch(f[0])]
    he_enc, he = _filas(s23, "Codigo", "Herramienta", "Capa", "Justificacion")
    herramientas = [{"codigo": f[0], "herramienta": VI._col(he_enc, f, "Herramienta"), "capa": VI._col(he_enc, f, "Capa"),
                     "funcion": VI._col(he_enc, f, "Funcion"), "justificacion": VI._col(he_enc, f, "Justificacion"),
                     "alternativa": VI._col(he_enc, f, "Alternativa")} for f in he if f and re.fullmatch(r"HER-\d+", f[0])]
    return {"decisiones": vinetas(s21, "Decisiones que apoya"), "usuarios": VI.campo(s21, "Usuarios"),
            "respuesta": VI.campo(s21, "Respuesta a la problemática"), "objetivos": objetivos,
            "componentes": componentes, "lectura": VI.campo(s22, "Lectura de la arquitectura"), "herramientas": herramientas}


def leer_modelo(run):
    """Datos de 2.4 y 2.5 de una corrida de 07-make-data-model-kpi (y `modelo.json` si existe y es válido)."""
    s24, s25 = _seccion(run, "2.4"), _seccion(run, "2.5")
    h_enc, h = _filas(s24, "Codigo", "Granularidad", "Medidas")
    hechos = [{"codigo": f[0], "nombre": VI._col(h_enc, f, "Tabla"), "granularidad": VI._col(h_enc, f, "Granularidad"),
               "medidas": _medidas(VI._col(h_enc, f, "Medidas")), "claves": _partes(VI._col(h_enc, f, "Claves"))}
              for f in h if f and re.fullmatch(r"FCT-\d+", f[0])]
    d_enc, d = _filas(s24, "Codigo", "Clave", "Atributos")
    dimensiones = [{"codigo": f[0], "nombre": VI._col(d_enc, f, "Dimension"), "clave": VI._col(d_enc, f, "Clave"),
                    "atributos": _partes(VI._col(d_enc, f, "Atributos")), "jerarquias": _partes(VI._col(d_enc, f, "Jerarquias"))}
                   for f in d if f and re.fullmatch(r"DIM-\d+", f[0])]
    r_enc, r = _filas(s24, "Codigo", "Desde", "Hacia")
    relaciones = [{"codigo": f[0], "desde": VI._col(r_enc, f, "Desde"), "hacia": VI._col(r_enc, f, "Hacia"), "campos": VI._col(r_enc, f, "Campos"),
                   "cardinalidad": VI._col(r_enc, f, "Cardinalidad"), "filtro": VI._col(r_enc, f, "Filtro")}
                  for f in r if f and re.fullmatch(r"REL-\d+", f[0])]
    k1_enc, k1 = _filas(s25, "Codigo", "Formula", "Medida")
    k2_enc, k2 = _filas(s25, "Codigo", "Meta", "Frecuencia", "Objetivo")
    gestion = {f[0]: f for f in k2 if f}
    kpis = []
    for f in k1:
        if not f or not re.fullmatch(r"KPI-\d+", f[0]):
            continue
        g = gestion.get(f[0])
        kpis.append({"codigo": f[0], "nombre": VI._col(k1_enc, f, "KPI"), "formula": VI._col(k1_enc, f, "Formula"),
                     "medida": VI._col(k1_enc, f, "Medida"), "origen": _partes(VI._col(k1_enc, f, "Origen")),
                     "meta": VI._col(k2_enc, g, "Meta") if g else "", "frecuencia": VI._col(k2_enc, g, "Frecuencia") if g else "",
                     "objetivo": VI._col(k2_enc, g, "Objetivo") if g else "", "decision": VI._col(k2_enc, g, "Decision") if g else "",
                     "con_gestion": g is not None})
    js, js_error = None, None
    f = Path(run) / "modelo.json"
    if f.is_file():
        try:
            js = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            js_error = str(e)
    return {"hechos": hechos, "dimensiones": dimensiones, "relaciones": relaciones, "kpis": kpis,
            "lectura": VI.campo(s24, "Lectura del modelo"), "lectura_kpi": VI.campo(s25, "Lectura de los KPI"),
            "json": js, "json_error": js_error}


LECTORES = {NEGOCIO: leer_negocio, ESTRATEGICO: leer_estrategico, PROBLEMA: leer_problema, SOLUCION: leer_solucion, MODELO: leer_modelo}


def leer(raiz, paso, run=None):
    return LECTORES[paso](corrida(raiz, paso, run))


# ------------------------------------------------------------------ comprobaciones comunes
def _rel(punto):
    return f"secciones/{punto}.md"


def check_encabezados(run, puntos):
    inc = []
    for p in puntos:
        t = texto(run, p)
        if t is None:
            inc.append((_rel(p), f"falta el archivo (sección {p} del informe)"))
            continue
        primera = next((ln.strip() for ln in t.splitlines() if ln.strip()), "")
        if primera != encabezado(p):
            inc.append((_rel(p), f"la primera línea debe ser «{encabezado(p)}» (está «{primera[:80]}»)"))
        otros = [ln for ln in t.splitlines()[1:] if re.match(r"^#{1,2}\s", ln)]
        if otros:
            inc.append((_rel(p), f"tiene otro encabezado de nivel 1 o 2 («{otros[0].strip()[:60]}»); usa ### o rótulos en negrita"))
    return inc


def check_figuras(run, puntos):
    inc = []
    run = Path(run)
    for p in puntos:
        t = texto(run, p)
        if t is None:
            continue
        marcas = [RE_FIGURA.match(ln.strip()).group(1) for ln in t.splitlines() if RE_FIGURA.match(ln.strip())]
        comentarios = [ln for ln in t.splitlines() if "<!--" in ln and not RE_FIGURA.match(ln.strip())]
        if comentarios:
            inc.append((_rel(p), f"comentario que no es una marca de figura: «{comentarios[0].strip()[:60]}» (el texto es final, sin notas)"))
        esperado = FIGURAS.get(p)
        if esperado and marcas != esperado:
            lineas = " y ".join(f"«<!-- figura: {v} -->»" for v in esperado)
            inc.append((_rel(p), f"debe marcar {'una sola vez la figura con la línea' if len(esperado) == 1 else 'en este orden, una vez cada una, las figuras con las líneas'} {lineas}"))
        if not esperado and marcas:
            inc.append((_rel(p), f"la sección {p} no lleva imagen y marca la figura {marcas[0]}"))
        for v in marcas:
            if v not in VI.VISUALES:
                inc.append((_rel(p), f"visual desconocido en la marca de figura: {v}"))
                continue
            if not (run / "visuales" / f"{v}.html").is_file():
                inc.append((f"visuales/{v}.html", f"falta el visual de la figura (visuales.py construir --visual {v} --run {run.name})"))
            leer_f = run / "leer-imagen" / f"{v}.md"
            if not leer_f.is_file():
                inc.append((f"leer-imagen/{v}.md", "falta la explicación de la figura (la escribe visuales.py construir)"))
                continue
            datos_f = run / "visuales" / f"{v}.json"
            resaltado = False
            if datos_f.is_file():
                try:
                    resaltado = VI.resaltado(v, json.loads(datos_f.read_text(encoding="utf-8")))
                except (ValueError, KeyError, TypeError):
                    pass
            for c in VI.validar_explicacion(leer_f.read_text(encoding="utf-8"), resaltado):
                inc.append((f"leer-imagen/{v}.md", c))
    return inc


def check_marcador(run, puntos):
    inc = []
    for p in puntos:
        t = texto(run, p)
        if t and re.search(r"modelado por el agente", t, re.I):
            inc.append((_rel(p), "copia el marcador «(modelado por el agente, …)»: el informe va sin él y la procedencia va en README.md"))
    return inc


RE_CITA_P = re.compile(r"\(([A-ZÁÉÍÓÚÑ][^()]*?),\s*((?:19|20)\d{2}[a-z]?|s\. f\.)\)")
RE_CITA_N = re.compile(r"([A-ZÁÉÍÓÚÑ][^\s(),;|«»]*(?:\s+(?:y|&)\s+[A-ZÁÉÍÓÚÑ][^\s(),;|]*|\s+et al\.)?)\s+\(((?:19|20)\d{2}[a-z]?|s\. f\.)\)")


def citas(t):
    """[(autor, año)] de las citas en texto, en paréntesis «(Autor, año)» o narrativas «Autor (año)»."""
    out = []
    for m in RE_CITA_P.finditer(t):
        for parte in m.group(1).split(";"):
            out.append((parte.strip(), m.group(2)))
    for m in RE_CITA_N.finditer(t):
        out.append((m.group(1).strip(), m.group(2)))
    return out


def _token(autor):
    a = re.sub(r"\[[^\]]*\]", "", autor)
    a = re.split(r"\s+(?:y|&|et al\.)\s*|,", a)[0].strip()
    return a.split()[0].strip(".") if a.split() else ""


def check_citas(run, puntos):
    run = Path(run)
    ref_f = run / "referencias.md"
    refs = [ln.strip().lstrip("-* ").strip() for ln in ref_f.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")] if ref_f.is_file() else []
    inc = []
    for i, r in enumerate(refs, 1):
        if not re.search(r"\((?:(?:19|20)\d{2}[a-z]?(?:, [^)]+)?|s\. f\.)\)", r):
            inc.append(("referencias.md", f"línea {i}: la referencia no tiene el año entre paréntesis (APA 7)"))
    vistos = set()
    for p in puntos:
        t = texto(run, p)
        if not t:
            continue
        for autor, anio in citas(t):
            tok = _token(autor)
            if not tok or (tok, anio) in vistos:
                continue
            vistos.add((tok, anio))
            ok = any(anio in r and (tok.lower() in r.lower() or tok.isupper()) for r in refs)
            if not ok:
                donde = "referencias.md" if refs else "referencias.md (no existe)"
                inc.append((_rel(p), f"cita sin referencia: {autor}, {anio} (agrégala a {donde})"))
    return inc


def check_comunes(run, puntos):
    """Encabezados, figuras, marcador de datos modelados y citas de las secciones `puntos` de la corrida."""
    return check_encabezados(run, puntos) + check_figuras(run, puntos) + check_marcador(run, puntos) + check_citas(run, puntos)


def faltan_secciones(inc):
    return any("falta el archivo" in m for _, m in inc)


# ------------------------------------------------------------------ dominio
def dominio(raiz):
    """{'secciones': {...}, 'datos': {...}} de project/domain.md sin marcadores (vacío si no existe)."""
    try:
        cfg = P.load(raiz)
        f = Path(raiz) / cfg["dominio"]
    except P.ConfigError:
        f = Path(raiz) / "project" / "domain.md"
    if not f.is_file():
        return {"secciones": {}, "datos": {}}
    t = f.read_text(encoding="utf-8")
    sec = {k: MARCADOR.sub("", v).strip() for k, v in VI.secciones(t).items()}
    enc, filas = _filas(t, "Dato", "Valor")
    datos = {f[0]: MARCADOR.sub("", f[1]).strip() for f in filas if len(f) >= 2}
    return {"secciones": sec, "datos": datos}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    le = sub.add_parser("leer")
    le.add_argument("--paso", required=True, choices=sorted(LECTORES))
    le.add_argument("--run")
    le.add_argument("--raiz", default=".")
    sub.add_parser("titulos")
    a = ap.parse_args(argv)
    if a.cmd == "titulos":
        for p, t in titulos().items():
            print(f"## {p}. {t}")
        return 0
    try:
        print(json.dumps(leer(Path(a.raiz).resolve(), a.paso, a.run), ensure_ascii=False, indent=2))
        return 0
    except (SinCorrida, P.ConfigError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
