"""Reglas del paso 08-make-etl (sección 3.1, anexos A y B y evidencia.json; se invocan desde validate_run.py)."""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import brief as BR  # noqa: E402
import diagnostico as D  # noqa: E402
import etl_verificacion as EV  # noqa: E402
import projectcfg as P  # noqa: E402
import visuales as VI  # noqa: E402

PASO = "08-make-etl"
PUNTOS = ["3.1"]
UPDATE = "08-make-etl-update"
PREFIJOS = ("REG", "PAS")
DEFECTOS = ("registro_invalido", "duplicado", "nombre_producto", "formato_fecha", "nulo", "dia_sin_precio")
ENC_A = "# Anexo A: Diccionario de datos y calidad de datos"
ENC_B = "# Anexo B: Scripts del ETL"
RE_NUM_FILAS = re.compile(r"(\d[\d\s.]*\d|\d)\s+(?:filas|registros|líneas|lineas)\b", re.I)
RE_ORIGEN = re.compile(r"^(?:FUE-\d+|apoyo-[a-z-]+)\.\S+$")  # fuente del brief o archivo de apoyo (apoyo-catalogo-productos.campo)
S31, EVIDENCIA = "secciones/3.1.md", "evidencia.json"


# ------------------------------------------------------------------ lectura
def _int(s):
    s = str(s if s is not None else "").replace("−", "-").strip()
    s = re.sub(r"[^\d-]", "", s)
    return int(s) if re.fullmatch(r"-?\d+", s) else None


def _tabla(txt, *cols):
    """Filas ({columna normalizada: celda}) de la primera tabla cuyo encabezado tiene exactamente esas columnas; None si no hay."""
    quiero = [VI._norm(c) for c in cols]
    for enc, filas in VI.tablas(txt):
        e = [VI._norm(x) for x in enc]
        if all(q in e for q in quiero):
            return [{e[i]: f[i] for i in range(min(len(e), len(f)))} for f in filas]
    return None


def _c(fila, col):
    return fila.get(VI._norm(col), "").strip()


def _sin_codigo(t):
    return re.sub(r"```.*?```", "", t, flags=re.S)


def _titulos(texto, archivo):
    """Cada tabla lleva antes su línea `Tabla N: título`."""
    inc, lin = [], _sin_codigo(texto).splitlines()
    for k, l in enumerate(lin):
        if l.strip().startswith("|") and (k == 0 or not lin[k - 1].strip().startswith("|")):
            previa = next((x for x in reversed(lin[:k]) if x.strip()), "")
            if not re.match(r"^Tabla \d+: \S", previa.strip()):
                inc.append((archivo, "hay una tabla sin su título «Tabla N: …» en la línea anterior"))
    return inc


def campos_modelo(m):
    """{tabla: {campos}} de hechos (claves y medidas) y dimensiones (clave y atributos) de modelo.json."""
    out = {}
    for h in m.get("hechos", []):
        out[h["nombre"]] = set(h.get("claves", [])) | {x["nombre"] for x in h.get("medidas", [])}
    for x in m.get("dimensiones", []):
        out[x["nombre"]] = {x["clave"], *x.get("atributos", [])}
    return out


def _modelo(raiz):
    try:
        f = D.corrida(raiz, D.MODELO) / "modelo.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else None
    except (D.SinCorrida, P.ConfigError, ValueError, OSError):
        return None


def _defectos(raiz):
    f = Path(raiz) / "data" / "respuestas" / "defectos.csv"
    if not f.is_file():
        return None
    with open(f, newline="", encoding="utf-8-sig") as fh:
        return {r["defecto"].strip() for r in csv.DictReader(fh) if r.get("defecto")}


# ------------------------------------------------------------------ evidencia
def check_evidencia(run):
    """(evidencia o None, incidencias) de evidencia.json: existe, es JSON y tiene la forma del contrato."""
    f = Path(run) / EVIDENCIA
    if not f.is_file() and (Path(run) / "evidencia-desactualizada.json").is_file():
        return None, [(EVIDENCIA, "la evidencia quedó desactualizada porque se regeneraron los datos: el equipo debe repetir el ETL y traer la nueva (evidencia-desactualizada.json es la anterior)")]
    if not f.is_file():
        return None, [(EVIDENCIA, "falta la evidencia del equipo (filas antes y después de cada regla, filas por fuente y por tabla): pídesela y guárdala aquí")]
    try:
        ev = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        return None, [(EVIDENCIA, f"no es un JSON válido: {e}")]
    inc = []
    if ev.get("schema") != 1:
        inc.append((EVIDENCIA, "`schema` debe ser 1"))
    for i, r in enumerate(ev.get("reglas", []), 1):
        if not re.fullmatch(r"REG-\d+", str(r.get("codigo", ""))) or _int(r.get("filas_antes")) is None or _int(r.get("filas_despues")) is None:
            inc.append((EVIDENCIA, f"reglas[{i}]: necesita `codigo` (REG-nn), `filas_antes` y `filas_despues` enteros"))
    for i, t in enumerate(ev.get("tablas", []), 1):
        if not str(t.get("nombre", "")).strip() or _int(t.get("filas")) is None:
            inc.append((EVIDENCIA, f"tablas[{i}]: necesita `nombre` y `filas` entero"))
    v = ev.get("verificacion")
    if v is not None and v.get("estado") not in ("coincide", "diferencias"):
        inc.append((EVIDENCIA, "`verificacion.estado` debe ser «coincide» o «diferencias» (lo escribe etl_verificacion.py comparar --actualizar)"))
    return ev, inc


def _numeros(ev):
    """Cifras que la evidencia respalda (enteras)."""
    out = set()
    for r in ev.get("reglas", []):
        out |= {_int(r.get("filas_antes")), _int(r.get("filas_despues"))}
    for t in ev.get("tablas", []):
        out.add(_int(t.get("filas")))
    out.add(_int((ev.get("totales") or {}).get("lineas_total")))
    for d in (ev.get("verificacion") or {}).get("diferencias", []):
        out |= {_int(d.get("esperado")), _int(d.get("obtenido")), abs(_int(d.get("desvio")) or 0)}
    out.discard(None)
    return out


# ------------------------------------------------------------------ sección 3.1
def reglas_de(txt):
    return _tabla(txt, "Código", "Regla", "Defecto que trata", "Tabla", "Filas antes", "Filas después") or []


def pasos_de(txt):
    return _tabla(txt, "Código", "Paso", "Tabla", "Resultado") or []


def check_fuentes(t, ev, br):
    inc = []
    filas = _tabla(t, "Código", "Fuente", "Archivo", "Filas leídas")
    if filas is None:
        return [(S31, "falta la tabla de extracción «Código | Fuente | Archivo | Filas leídas»")]
    en_tabla = {_c(f, "Código"): f for f in filas}
    tablas = {x.get("nombre"): _int(x.get("filas")) for x in ev.get("tablas", [])}
    for fu in (br or {}).get("fuentes", []):
        c = fu["codigo"]
        if c not in en_tabla:
            inc.append((S31, f"{c}: la fuente del brief no está en la tabla de extracción"))
    for c, f in en_tabla.items():
        if c not in tablas:
            inc.append((S31, f"{c}: las filas leídas no están en la evidencia (tablas: nombre «{c}»)"))
        elif _int(_c(f, "Filas leídas")) != tablas[c]:
            inc.append((S31, f"{c}: la tabla dice {_c(f, 'Filas leídas')} filas leídas y la evidencia {tablas[c]}"))
    return inc


def check_pasos(t):
    filas = pasos_de(t)
    if not filas:
        return [(S31, "falta la tabla de pasos «Código | Paso | Tabla | Resultado» con al menos un PAS-nn")]
    return []


def check_reglas(t, ev, raiz):
    inc, filas = [], reglas_de(t)
    if not filas:
        return [(S31, "falta la tabla de reglas «Código | Regla | Defecto que trata | Tabla | Criterio de aceptación | Filas antes | Filas después»")]
    en_ev = {r.get("codigo"): r for r in ev.get("reglas", [])}
    tratados = set()
    for f in filas:
        c, d = _c(f, "Código"), _c(f, "Defecto que trata").strip("`")
        if d not in DEFECTOS:
            inc.append((S31, f"{c}: el defecto «{d}» debe ser uno de {', '.join(DEFECTOS)}"))
        tratados.add(d)
        e = en_ev.get(c)
        if e is None:
            inc.append((S31, f"{c}: la regla no tiene filas antes y después en la evidencia"))
            continue
        for col, clave in (("Filas antes", "filas_antes"), ("Filas después", "filas_despues")):
            if _int(_c(f, col)) != _int(e.get(clave)):
                inc.append((S31, f"{c}: «{col.lower()}» dice {_c(f, col)} y la evidencia {e.get(clave)}"))
    esperados = _defectos(raiz)
    for d in sorted((esperados or set()) - tratados):
        inc.append((S31, f"el defecto «{d}» de data/respuestas/defectos.csv no tiene una regla REG-nn que lo trate"))
    return inc


def check_carga(t, ev, modelo):
    filas = _tabla(t, "Tabla", "Filas cargadas")
    if filas is None:
        return [(S31, "falta la tabla de carga «Tabla | Filas cargadas»")]
    inc = []
    tablas = {x.get("nombre"): _int(x.get("filas")) for x in ev.get("tablas", [])}
    en_tabla = {_c(f, "Tabla"): f for f in filas}
    for nombre in sorted(campos_modelo(modelo or {})):
        if nombre not in en_tabla:
            inc.append((S31, f"{nombre}: la tabla del modelo no está en la tabla de carga"))
    for nombre, f in en_tabla.items():
        if nombre not in tablas:
            inc.append((S31, f"{nombre}: las filas cargadas no están en la evidencia"))
        elif _int(_c(f, "Filas cargadas")) != tablas[nombre]:
            inc.append((S31, f"{nombre}: la tabla dice {_c(f, 'Filas cargadas')} filas cargadas y la evidencia {tablas[nombre]}"))
    return inc


def check_verificacion(t, ev, raiz):
    v = ev.get("verificacion")
    texto = VI.campo(t, "Verificación")
    if not texto:
        return [(S31, "falta la «**Verificación.**» con el resultado de la comparación con la hoja de respuestas")]
    if v is None:
        if (Path(raiz) / "data" / "respuestas").is_dir():
            return [(EVIDENCIA, "falta `verificacion`: ejecuta etl_verificacion.py comparar --evidencia <ruta> --actualizar")]
        return []
    inc, dif = [], v.get("diferencias", [])
    if v.get("estado") == "coincide":
        if "coincid" not in texto.lower():
            inc.append((S31, "la evidencia dice que los totales coinciden y la «Verificación» no lo dice"))
    else:
        if "diferencia" not in texto.lower():
            inc.append((S31, "la evidencia tiene diferencias y la «Verificación» no las menciona"))
        filas = _tabla(t, "Tabla", "Mes", "Esperado", "Obtenido")
        if filas is None or len(filas) != len(dif):
            inc.append((S31, f"la evidencia tiene {len(dif)} diferencias y la tabla «Tabla | Mes | Esperado | Obtenido | Diferencia» {'no existe' if filas is None else f'tiene {len(filas)}'}"))
    if (Path(raiz) / "data" / "respuestas").is_dir():
        ahora = EV.comparar(raiz, ev)
        if ahora["estado"] in ("coincide", "diferencias") and ahora["estado"] != v.get("estado"):
            inc.append((EVIDENCIA, f"la verificación guardada dice «{v.get('estado')}» y la comparación actual con data/respuestas/ dice «{ahora['estado']}»: vuelve a ejecutar etl_verificacion.py comparar --actualizar"))
    return inc


def check_cifras_en_texto(t, ev):
    """Toda cantidad de filas citada en la prosa está en la evidencia."""
    prosa = "\n".join(l for l in _sin_codigo(t).splitlines() if not l.strip().startswith("|"))
    validas, inc = _numeros(ev), []
    for m in RE_NUM_FILAS.finditer(prosa):
        n = _int(m.group(1))
        if n not in validas:
            inc.append((S31, f"cita {m.group(0).strip()} y esa cantidad no está en la evidencia"))
    return inc


def check_costos(t, raiz, modelo):
    """Con archivos de apoyo en data/, 3.1 explica cómo se calculan los costos del modelo que dependen de ellos."""
    if not list((Path(raiz) / "data").glob("apoyo-*.csv")):
        return []
    campos = {c for cs in campos_modelo(modelo or {}).values() for c in cs}
    inc = []
    for campo, rx in (("costo_estimado", r"costo[_ ]estimado"), ("costo_operativo", r"costo[_ ]operativo")):
        if campo in campos and not re.search(rx, t, re.I):
            inc.append((S31, f"el modelo tiene {campo} y 3.1 no explica cómo se calcula con los archivos de apoyo de data/"))
    return inc


def check_seccion(run, raiz, ev, br, modelo):
    t = D.texto(run, "3.1")
    cfg = None
    try:
        cfg = P.load(raiz)
    except P.ConfigError:
        pass
    inc = _titulos(t, S31)
    if cfg and cfg.get("modo_datos") == "generado" and not re.search(r"generad[oa]s?", t, re.I):
        inc.append((S31, "el proyecto usa datos generados y 3.1 no lo declara (di que los datos son generados para el proyecto y cómo se calibraron)"))
    inc += check_costos(t, raiz, modelo)
    if not VI.campo(t, "Lectura del ETL"):
        inc.append((S31, "falta la «**Lectura del ETL.**»"))
    if ev is None:
        return inc
    return inc + check_fuentes(t, ev, br) + check_pasos(t) + check_reglas(t, ev, raiz) + check_carga(t, ev, modelo) \
        + check_verificacion(t, ev, raiz) + check_cifras_en_texto(t, ev)


# ------------------------------------------------------------------ anexos
def _anexo(run, letra, encabezado):
    f = Path(run) / "anexos" / f"{letra}.md"
    if not f.is_file():
        return None, [(f"anexos/{letra}.md", f"falta el anexo {letra} de esta sección")]
    t = f.read_text(encoding="utf-8")
    primera = next((l.strip() for l in t.splitlines() if l.strip()), "")
    inc = [] if primera == encabezado else [(f"anexos/{letra}.md", f"la primera línea debe ser «{encabezado}» (está «{primera[:70]}»)")]
    return t, inc


def check_anexo_a(run, t31, ev, br, modelo):
    A = "anexos/A.md"
    t, inc = _anexo(run, "A", ENC_A)
    if t is None:
        return inc
    inc += _titulos(t, A)
    reglas31 = {_c(f, "Código") for f in reglas_de(t31)}
    destinos = {f"{tb}.{c}" for tb, cs in campos_modelo(modelo or {}).items() for c in cs}
    dic = _tabla(t, "Fuente", "Campo", "Tipo", "Regla de calidad", "Destino")
    if dic is None:
        inc.append((A, "falta el diccionario «Fuente | Campo | Tipo | Regla de calidad | Destino»"))
    else:
        vistas = {_c(f, "Fuente") for f in dic}
        for fu in (br or {}).get("fuentes", []):
            if fu["codigo"] not in vistas:
                inc.append((A, f"{fu['codigo']}: la fuente del brief no tiene campos en el diccionario"))
        for f in dic:
            r, d = _c(f, "Regla de calidad"), _c(f, "Destino")
            if r not in ("—", "-", "") and r not in reglas31:
                inc.append((A, f"{_c(f, 'Fuente')}.{_c(f, 'Campo')}: la regla {r} no está definida en 3.1"))
            if modelo and d not in ("—", "-", "") and d not in destinos:
                inc.append((A, f"{_c(f, 'Fuente')}.{_c(f, 'Campo')}: el destino «{d}» no existe en el modelo"))
    org = _tabla(t, "Tabla", "Campo", "Origen")
    if org is None:
        inc.append((A, "falta el origen de los campos del modelo «Tabla | Campo | Origen»"))
    elif modelo:
        fuentes = {x["codigo"] for x in br["fuentes"]} if br else None
        cubiertos = {}
        for f in org:
            tb = _c(f, "Tabla")
            origenes = [x.strip() for x in _c(f, "Origen").split(";") if x.strip()]
            if not origenes:
                inc.append((A, f"{tb}: la fila de «{_c(f, 'Campo')}» no tiene origen"))
            for o in origenes:
                if o.lower().startswith("cálculo"):
                    continue
                es_fuente = o.startswith("FUE-")
                if not RE_ORIGEN.match(o) or (es_fuente and fuentes is not None and o.split(".")[0] not in fuentes):
                    inc.append((A, f"{tb}: el origen «{o}» debe ser FUE-nn.campo de una fuente del brief, apoyo-<archivo>.campo de un archivo de apoyo o «Cálculo: …»"))
            cubiertos.setdefault(tb, set()).update(x.strip() for x in _c(f, "Campo").split(";") if x.strip())
        campos = campos_modelo(modelo)
        for tb, cs in campos.items():
            for c in sorted(cs - cubiertos.get(tb, set())):
                inc.append((A, f"{tb}.{c}: el campo del modelo no tiene origen ni cálculo"))
        for tb, cs in cubiertos.items():
            for c in sorted(cs - campos.get(tb, set())):
                inc.append((A, f"{tb}.{c}: el campo no existe en el modelo"))
    res = _tabla(t, "Código", "Filas antes", "Filas después", "Diferencia")
    if res is None:
        inc.append((A, "falta el resultado de las reglas «Código | Filas antes | Filas después | Diferencia»"))
    elif ev is not None:
        en_ev = {r.get("codigo"): r for r in ev.get("reglas", [])}
        vistas = set()
        for f in res:
            c = _c(f, "Código")
            vistas.add(c)
            e = en_ev.get(c)
            if e is None:
                inc.append((A, f"{c}: la regla no está en la evidencia"))
                continue
            a, d = _int(_c(f, "Filas antes")), _int(_c(f, "Filas después"))
            if (a, d) != (_int(e.get("filas_antes")), _int(e.get("filas_despues"))):
                inc.append((A, f"{c}: las filas antes y después difieren de la evidencia ({e.get('filas_antes')} y {e.get('filas_despues')})"))
            if a is not None and d is not None and _int(_c(f, "Diferencia")) != d - a:
                inc.append((A, f"{c}: la diferencia debe ser {d - a}"))
        for c in sorted(reglas31 - vistas):
            inc.append((A, f"{c}: la regla de 3.1 no tiene su fila en el resultado"))
    return inc


def check_anexo_b(run, t31):
    B = "anexos/B.md"
    t, inc = _anexo(run, "B", ENC_B)
    if t is None:
        return inc
    partes = re.split(r"(?m)^\*\*(PAS-\d+)\.\*\*", t)
    bloques = {partes[i]: partes[i + 1] for i in range(1, len(partes) - 1, 2)}
    en31 = {_c(f, "Código") for f in pasos_de(t31)}
    for c in sorted(en31):
        b = bloques.get(c)
        if b is None:
            inc.append((B, f"{c}: el paso de 3.1 no tiene su bloque «**{c}.**» en el anexo B"))
        elif not any(x.strip() for x in re.findall(r"```[^\n]*\n(.*?)```", b, flags=re.S)) and not re.search(r"(?m)^\s*(?:\d+\.|[-*])\s+\S", b):
            inc.append((B, f"{c}: el bloque no trae el código ni los pasos que ejecutó el equipo"))
    for c in sorted(set(bloques) - en31):
        inc.append((B, f"{c}: el bloque del anexo B no corresponde a ningún paso de 3.1"))
    return inc


# ------------------------------------------------------------------ validación
def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    ev, inc_ev = check_evidencia(run)
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        br = None
        inc.append((S31, f"no se pueden comprobar las fuentes sin el brief vigente: {e}"))
    modelo = _modelo(raiz)
    if modelo is None:
        inc.append((S31, "no hay modelo.json en la corrida vigente de 07-make-data-model-kpi: sin él no se pueden comprobar las tablas ni los campos"))
    t31 = D.texto(run, "3.1")
    return inc + inc_ev + check_seccion(run, raiz, ev, br, modelo) + check_anexo_a(run, t31, ev, br, modelo) + check_anexo_b(run, t31)
