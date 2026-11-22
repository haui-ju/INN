"""Reglas del paso 05-make-problem-objectives (secciones 1.8 a 1.10; se invocan desde validate_run.py)."""
from pathlib import Path

import brief as BR
import diagnostico as D
import projectcfg as P
import visuales as VI

PASO = D.PROBLEMA
PUNTOS = ["1.8", "1.9", "1.10"]
UPDATE = "05-make-problem-objectives-update"
PREFIJOS = ("OG", "OE")
MIN_PRINCIPALES, MAX_PRINCIPALES = 2, 4
CAMPOS_OBJ = ("objetivo", "metrica", "meta", "plazo", "aporta", "indicador")


def _vacio(t):
    return not (t or "").strip()


def check_problematica(d, causas):
    A = "secciones/1.8.md"
    inc = []
    for rot, clave in (("Enunciado", "enunciado"), ("Afectados", "afectados")):
        if _vacio(d[clave]):
            inc.append((A, f"falta «**{rot}.**»"))
    if not d["evidencia"]:
        inc.append((A, "falta la «**Evidencia.**» (al menos una viñeta)"))
    n = len(d["principales"])
    if not MIN_PRINCIPALES <= n <= MAX_PRINCIPALES:
        inc.append((A, f"hay {n} causas principales; deben ser entre {MIN_PRINCIPALES} y {MAX_PRINCIPALES}, tomadas del Ishikawa"))
    if causas is None:
        return inc
    por = {c["codigo"]: c for c in causas}
    for p in d["principales"]:
        c = por.get(p["codigo"])
        if c is None:
            inc.append((A, f"{p['codigo']}: no está en el Ishikawa vigente (agrégala con 04-make-strategic-analysis-update o elige otra)"))
            continue
        if D.norm(p["causa"]) != D.norm(c["causa"]):
            inc.append((A, f"{p['codigo']}: el texto difiere del Ishikawa («{c['causa']}»)"))
        if D.norm(p["categoria"]) != D.norm(c["categoria"]):
            inc.append((A, f"{p['codigo']}: la categoría debe ser «{c['categoria']}», como en el Ishikawa"))
        if _vacio(p["evidencia"]):
            inc.append((A, f"{p['codigo']}: falta la evidencia"))
    return inc


def _compara(archivo, propios, del_brief, nombre):
    inc = []
    a = {o["codigo"]: o for o in propios}
    b = {o["codigo"]: o for o in del_brief}
    for c in b:
        if c not in a:
            inc.append((archivo, f"falta {c} (se copia del brief)"))
    for c, o in a.items():
        if c not in b:
            inc.append((archivo, f"{c} no está en el brief vigente: los {nombre} se copian del brief, no se proponen aquí"))
            continue
        for campo in CAMPOS_OBJ:
            if D.norm(o[campo]) != D.norm(b[c][campo]):
                inc.append((archivo, f"{c}: «{campo}» difiere del brief; cópialo sin cambios o cambia el objetivo con 01-make-project-brief-update"))
    return inc


def check_objetivos(d, br):
    return (_compara("secciones/1.9.md", d["og"], br["og"], "objetivos generales")
            + _compara("secciones/1.10.md", d["oe"], br["oe"], "objetivos específicos"))


def check_matriz(d, br, est, neg):
    A = "secciones/1.10.md"
    inc = []
    if not d["matriz"]:
        return [(A, "falta la «**Matriz de articulación.**» con la tabla «Objetivo | Causas (Ishikawa) | FODA | PESTEL | Canvas | Indicador»")]
    oe = {o["codigo"]: o for o in br["oe"]}
    filas = {f["objetivo"]: f for f in d["matriz"]}
    for c in oe:
        if c not in filas:
            inc.append((A, f"la matriz no tiene la fila de {c}"))
    causas = {c["codigo"] for c in est["causas"]} if est else None
    foda = ({i["codigo"] for v in est["foda"].values() for i in v} | {e["codigo"] for e in est["estrategias"]}) if est else None
    pestel = {i["codigo"] for i in est["pestel"]} if est else None
    bloques = {D.norm(b["bloque"]) for b in neg["canvas"]} if neg else {D.norm(b) for b in D.BLOQUES_BMC}
    for f in d["matriz"]:
        c = f["objetivo"]
        if c not in oe:
            inc.append((A, f"la matriz tiene la fila {c}, que no es un objetivo específico del brief"))
            continue
        if not f["causas"]:
            inc.append((A, f"{c}: la fila no cita causas del Ishikawa (CAU-nn)"))
        if not f["foda"]:
            inc.append((A, f"{c}: la fila no cita ítems ni estrategias FODA"))
        if not f["pestel"] and D.norm(f["pestel_txt"]) not in ("—", "-", "–"):
            inc.append((A, f"{c}: la columna PESTEL cita códigos POL, ECO, SOC, TEC, AMB o LEG, o lleva «—»"))
        if not f["canvas"]:
            inc.append((A, f"{c}: la fila no cita bloques del Canvas"))
        for b in f["canvas"]:
            if D.norm(b) not in bloques:
                inc.append((A, f"{c}: «{b}» no es un bloque del Canvas (usa los nombres exactos de 1.4)"))
        for grupo, validos, nombre in ((f["causas"], causas, "el Ishikawa"), (f["foda"], foda, "la matriz FODA"), (f["pestel"], pestel, "el PESTEL")):
            if validos is None:
                continue
            for x in grupo:
                if x not in validos:
                    inc.append((A, f"{c}: cita {x}, que no está en {nombre} vigente"))
        if D.norm(f["indicador"]) != D.norm(oe[c]["indicador"]):
            inc.append((A, f"{c}: el indicador debe ser el del brief («{oe[c]['indicador']}»)"))
    citadas = {x for f in d["matriz"] for x in f["causas"]}
    for p in d["principales"]:
        if p["codigo"] not in citadas:
            inc.append((A, f"la causa principal {p['codigo']} no está articulada con ningún objetivo específico"))
    if _vacio(VI.campo(D.texto(Path(d["_run"]), "1.10"), "Lectura de la matriz")):
        inc.append((A, "falta la «**Lectura de la matriz.**»"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = D.leer_problema(run)
    d["_run"] = str(run)
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        return inc + [("secciones/1.9.md", f"no se pueden comprobar los objetivos sin el brief vigente: {e}")]
    est = neg = None
    try:
        est = D.leer(raiz, D.ESTRATEGICO)
    except (D.SinCorrida, P.ConfigError) as e:
        inc.append(("secciones/1.10.md", f"no se puede comprobar la matriz sin la corrida vigente de {D.ESTRATEGICO}: {e}"))
    try:
        neg = D.leer(raiz, D.NEGOCIO)
    except (D.SinCorrida, P.ConfigError) as e:
        inc.append(("secciones/1.10.md", f"no se pueden comprobar los bloques del Canvas sin la corrida vigente de {D.NEGOCIO}: {e}"))
    return (inc + check_problematica(d, est["causas"] if est else None) + check_objetivos(d, br)
            + check_matriz(d, br, est, neg))
