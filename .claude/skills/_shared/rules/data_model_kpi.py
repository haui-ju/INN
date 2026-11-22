"""Reglas del paso 07-make-data-model-kpi (secciones 2.4 y 2.5 y modelo.json; se invocan desde validate_run.py)."""
import re
from pathlib import Path

import brief as BR
import diagnostico as D
import projectcfg as P

PASO = D.MODELO
PUNTOS = ["2.4", "2.5"]
UPDATE = "07-make-data-model-kpi-update"
PREFIJOS = ("FCT", "DIM", "REL", "KPI")
TIPOS_MEDIDA = ("entero", "decimal")
RE_TIEMPO = re.compile(r"calendario|tiempo|fecha", re.I)


def _vacio(t):
    return not (t or "").strip()


def campos(d):
    """{tabla: {campos}} de hechos (medidas y claves) y dimensiones (clave y atributos)."""
    out = {}
    for h in d["hechos"]:
        out[h["nombre"]] = {m["nombre"] for m in h["medidas"]} | set(h["claves"])
    for x in d["dimensiones"]:
        out[x["nombre"]] = {x["clave"], *x["atributos"]}
    return out


def check_hechos(d):
    A = "secciones/2.4.md"
    inc = []
    if not d["hechos"]:
        return [(A, "falta la tabla de hechos «Código | Tabla de hechos | Granularidad | Medidas | Claves»")]
    for h in d["hechos"]:
        c = h["codigo"]
        if _vacio(h["nombre"]):
            inc.append((A, f"{c}: falta el nombre de la tabla de hechos"))
        if _vacio(h["granularidad"]):
            inc.append((A, f"{c}: la tabla de hechos {h['nombre']} no declara su granularidad"))
        if not h["medidas"]:
            inc.append((A, f"{c}: la tabla de hechos {h['nombre']} no tiene medidas"))
        for m in h["medidas"]:
            if D.norm(m["agregacion"]) not in D.AGREGACIONES:
                inc.append((A, f"{c}: la medida «{m['nombre']}» necesita su agregación entre paréntesis ({', '.join(D.AGREGACIONES)})"))
        if not h["claves"]:
            inc.append((A, f"{c}: la tabla de hechos {h['nombre']} no tiene claves hacia las dimensiones"))
    return inc


def check_dimensiones(d):
    A = "secciones/2.4.md"
    inc = []
    if not d["dimensiones"]:
        return [(A, "falta la tabla de dimensiones «Código | Dimensión | Clave | Atributos | Jerarquías»")]
    for x in d["dimensiones"]:
        if _vacio(x["nombre"]) or _vacio(x["clave"]):
            inc.append((A, f"{x['codigo']}: falta el nombre o la clave de la dimensión"))
        if not x["atributos"]:
            inc.append((A, f"{x['codigo']}: la dimensión {x['nombre']} no tiene atributos"))
    periodicos = [k for k in d["kpis"] if D.norm(k["frecuencia"]) in D.PERIODICAS]
    if periodicos and not any(RE_TIEMPO.search(x["nombre"]) for x in d["dimensiones"]):
        for k in periodicos:
            inc.append((A, f"{k['codigo']} tiene frecuencia {k['frecuencia'].lower()} y el modelo no tiene dimensión de tiempo (dCalendario)"))
    return inc


def check_relaciones(d):
    A = "secciones/2.4.md"
    inc = []
    hechos = {h["nombre"]: h for h in d["hechos"]}
    dims = {x["nombre"]: x for x in d["dimensiones"]}
    if not d["relaciones"]:
        return [(A, "falta la tabla de relaciones «Código | Desde | Hacia | Campos | Cardinalidad | Filtro»")]
    unidas = set()
    for r in d["relaciones"]:
        c = r["codigo"]
        ok = True
        if r["desde"] not in hechos:
            inc.append((A, f"{c}: «{r['desde']}» no es una tabla de hechos definida"))
            ok = False
        if r["hacia"] not in dims:
            inc.append((A, f"{c}: «{r['hacia']}» no es una dimensión definida"))
            ok = False
        if D.norm(r["cardinalidad"]) not in D.CARDINALIDADES:
            inc.append((A, f"{c}: la cardinalidad debe ser una de {', '.join(D.CARDINALIDADES)}"))
        if D.norm(r["filtro"]) not in {x.lower() for x in D.FILTROS}:
            inc.append((A, f"{c}: la dirección del filtro debe ser {' o '.join(D.FILTROS)}"))
        if not ok:
            continue
        unidas.add(r["hacia"])
        a, _, b = (x.strip() for x in re.partition(r"→|->", r["campos"])) if re.search(r"→|->", r["campos"]) else (r["campos"].strip(), "", r["campos"].strip())
        if a not in hechos[r["desde"]]["claves"]:
            inc.append((A, f"{c}: el campo «{a}» no está entre las claves de {r['desde']}"))
        if b != dims[r["hacia"]]["clave"]:
            inc.append((A, f"{c}: el campo «{b}» no es la clave de {r['hacia']} ({dims[r['hacia']]['clave']})"))
    for x in d["dimensiones"]:
        if x["nombre"] not in unidas:
            inc.append((A, f"{x['codigo']}: la dimensión {x['nombre']} no participa en ninguna relación"))
    if _vacio(d["lectura"]):
        inc.append((A, "falta la «**Lectura del modelo.**»"))
    return inc


def check_kpis(d, br):
    A = "secciones/2.5.md"
    inc = []
    if not d["kpis"]:
        return [(A, "faltan las tablas de KPI «Código | KPI | Fórmula | Medida propuesta | Origen» y «Código | Meta | Frecuencia | Objetivo | Decisión que apoya»")]
    tablas = campos(d)
    oe = {o["codigo"]: o for o in br["oe"]} if br else None
    for k in d["kpis"]:
        c = k["codigo"]
        if not k["con_gestion"]:
            inc.append((A, f"{c}: no tiene fila en la tabla de meta, frecuencia y decisión"))
            continue
        for rot, clave in (("la fórmula", "formula"), ("la medida propuesta", "medida"), ("la decisión que apoya", "decision")):
            if _vacio(k[clave]):
                inc.append((A, f"{c}: falta {rot}"))
        if _vacio(k["meta"]):
            inc.append((A, f"{c}: falta la meta (escribe la cifra con su comparador o «Pendiente»)"))
        if D.norm(k["frecuencia"]) not in {x.lower() for x in D.FRECUENCIAS}:
            inc.append((A, f"{c}: la frecuencia debe ser una de {', '.join(D.FRECUENCIAS)}"))
        if not k["origen"]:
            inc.append((A, f"{c}: falta el origen (campos del modelo como tabla.campo)"))
        for o in k["origen"]:
            tabla, _, campo = o.partition(".")
            if tabla not in tablas:
                inc.append((A, f"{c}: el origen «{o}» cita la tabla {tabla}, que no está en el modelo"))
            elif campo not in tablas[tabla]:
                inc.append((A, f"{c}: el campo «{o}» no está en el modelo de datos"))
        if oe is not None and k["objetivo"] not in oe:
            inc.append((A, f"{c}: el objetivo «{k['objetivo']}» no es un OE del brief vigente"))
    if oe is not None:
        for cod, o in oe.items():
            propios = [k for k in d["kpis"] if k["objetivo"] == cod]
            if not propios:
                inc.append((A, f"{cod}: el objetivo no tiene ningún KPI"))
            elif not any(D.norm(k["nombre"]) == D.norm(o["indicador"]) for k in propios):
                inc.append((A, f"{cod}: ningún KPI se llama como su indicador del brief («{o['indicador']}»)"))
    if _vacio(d["lectura_kpi"]):
        inc.append((A, "falta la «**Lectura de los KPI.**»"))
    return inc


def _cmp(inc, etiqueta, de_json, de_md, clave="codigo"):
    a = {x[clave]: x for x in de_json}
    b = {x[clave]: x for x in de_md}
    for c in sorted(set(a) - set(b)):
        inc.append(("modelo.json", f"{c} ({etiqueta}) está en modelo.json y no figura en las secciones"))
    for c in sorted(set(b) - set(a)):
        inc.append(("modelo.json", f"{c} ({etiqueta}) figura en las secciones y falta en modelo.json"))
    return [(a[c], b[c]) for c in sorted(set(a) & set(b))]


def check_json(d):
    J = "modelo.json"
    if d["json_error"]:
        return [(J, f"no es un JSON válido: {d['json_error']}")]
    j = d["json"]
    if j is None:
        return [(J, "falta modelo.json (el capítulo 3 lo lee: hechos, dimensiones, relaciones y KPI)")]
    inc = []
    for g in ("hechos", "dimensiones", "relaciones", "kpis"):
        if not isinstance(j.get(g), list):
            inc.append((J, f"falta la lista «{g}»"))
    if inc:
        return inc
    if j.get("schema") != 1:
        inc.append((J, "«schema» debe ser 1"))
    for a, b in _cmp(inc, "hecho", j["hechos"], d["hechos"]):
        c = b["codigo"]
        if D.norm(a.get("nombre")) != D.norm(b["nombre"]):
            inc.append((J, f"{c}: el nombre difiere de las secciones («{b['nombre']}»)"))
        if D.norm(a.get("granularidad")) != D.norm(b["granularidad"]):
            inc.append((J, f"{c}: la granularidad difiere de las secciones"))
        if [m.get("nombre") for m in a.get("medidas", [])] != [m["nombre"] for m in b["medidas"]]:
            inc.append((J, f"{c}: las medidas difieren de las secciones"))
        else:
            for m, n in zip(a.get("medidas", []), b["medidas"]):
                if D.norm(m.get("agregacion")) != D.norm(n["agregacion"]):
                    inc.append((J, f"{c}: la agregación de {n['nombre']} difiere de las secciones"))
                if m.get("tipo") not in TIPOS_MEDIDA:
                    inc.append((J, f"{c}: el tipo de {n['nombre']} debe ser {' o '.join(TIPOS_MEDIDA)}"))
        if list(a.get("claves", [])) != b["claves"]:
            inc.append((J, f"{c}: las claves difieren de las secciones"))
    for a, b in _cmp(inc, "dimensión", j["dimensiones"], d["dimensiones"]):
        c = b["codigo"]
        if D.norm(a.get("nombre")) != D.norm(b["nombre"]) or a.get("clave") != b["clave"]:
            inc.append((J, f"{c}: el nombre o la clave difieren de las secciones"))
        if list(a.get("atributos", [])) != b["atributos"] or list(a.get("jerarquias", [])) != b["jerarquias"]:
            inc.append((J, f"{c}: los atributos o las jerarquías difieren de las secciones"))
    for a, b in _cmp(inc, "relación", j["relaciones"], d["relaciones"]):
        c = b["codigo"]
        for clave in ("desde", "hacia", "campos", "cardinalidad", "filtro"):
            if D.norm(a.get(clave)) != D.norm(b[clave]):
                inc.append((J, f"{c}: «{clave}» difiere de las secciones («{b[clave]}»)"))
    for a, b in _cmp(inc, "KPI", j["kpis"], d["kpis"]):
        c = b["codigo"]
        for clave in ("nombre", "formula", "medida", "meta", "frecuencia", "objetivo", "decision"):
            if D.norm(a.get(clave)) != D.norm(b[clave]):
                inc.append((J, f"{c}: «{clave}» difiere de las secciones («{b[clave]}»)"))
        if list(a.get("origen", [])) != b["origen"]:
            inc.append((J, f"{c}: el origen difiere de las secciones"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = D.leer_modelo(run)
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        br = None
        inc.append(("secciones/2.5.md", f"no se pueden comprobar los objetivos sin el brief vigente: {e}"))
    return inc + check_hechos(d) + check_dimensiones(d) + check_relaciones(d) + check_kpis(d, br) + check_json(d)
