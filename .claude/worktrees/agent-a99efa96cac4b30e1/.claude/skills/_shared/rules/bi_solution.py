"""Reglas del paso 06-make-bi-solution (secciones 2.1 a 2.3; se invocan desde validate_run.py)."""
from collections import Counter
from pathlib import Path

import brief as BR
import diagnostico as D
import diseno as DS
import projectcfg as P

PASO = DS.SOLUCION
PUNTOS = ["2.1", "2.2", "2.3"]
UPDATE = "06-make-bi-solution-update"
PREFIJOS = ("CAP", "HER")
VISUALIZACION = "Visualización"


def _vacio(t):
    return not (t or "").strip() or D.norm(t) in ("—", "-", "–")


def _repetidos(codigos, archivo):
    return [(archivo, f"código repetido: {c}") for c, n in Counter(codigos).items() if n > 1]


def check_propuesta(d, br, principales):
    A = "secciones/2.1.md"
    inc = []
    if not d["decisiones"]:
        inc.append((A, "faltan las «**Decisiones que apoya.**» (al menos una viñeta, tomadas del brief)"))
    for rot, clave in (("Usuarios", "usuarios"), ("Respuesta a la problemática", "respuesta")):
        if _vacio(d[clave]):
            inc.append((A, f"falta «**{rot}.**»"))
    if principales is not None:
        for c in d["causas"]:
            if c not in principales:
                inc.append((A, f"la respuesta a la problemática cita {c}, que no es una causa principal de 1.8 vigente"))
    if not d["propuesta"]:
        return inc + [(A, "falta la tabla «Objetivo | Componentes | Cómo lo atiende»")]
    caps = {c["codigo"] for c in d["componentes"]}
    filas = {f["objetivo"] for f in d["propuesta"]}
    oe = [o["codigo"] for o in br["oe"]] if br else None
    if oe is not None:
        for c in oe:
            if c not in filas:
                inc.append((A, f"{c}: el objetivo del brief no tiene fila en la propuesta (indica los componentes que lo atienden)"))
    for f in d["propuesta"]:
        c = f["objetivo"]
        if oe is not None and c not in oe:
            inc.append((A, f"{c}: no es un objetivo específico del brief vigente"))
        if not f["componentes"]:
            inc.append((A, f"{c}: la fila no cita componentes de la arquitectura (CAP-nn)"))
        for x in f["componentes"]:
            if x not in caps:
                inc.append((A, f"{c}: cita {x}, que no está en la arquitectura de 2.2"))
        if _vacio(f["como"]):
            inc.append((A, f"{c}: falta «cómo lo atiende»"))
    return inc


def check_arquitectura(d, br):
    A = "secciones/2.2.md"
    inc = []
    comps = d["componentes"]
    if not comps:
        return [(A, "falta la tabla «Código | Capa | Componente | Función | Entrada | Salida»")]
    orden = []
    for c in comps:
        capa = DS.capa_canonica(c["capa"])
        if capa is None:
            inc.append((A, f"{c['codigo']}: capa «{c['capa']}» desconocida (usa {', '.join(DS.CAPAS)})"))
            continue
        orden.append((c["codigo"], DS.CAPAS.index(capa)))
        for campo, nombre in (("componente", "el componente"), ("funcion", "la función"), ("entrada", "la entrada"), ("salida", "la salida")):
            if _vacio(c[campo]):
                inc.append((A, f"{c['codigo']}: falta {nombre}"))
    presentes = {DS.CAPAS[i] for _, i in orden}
    for capa in DS.CAPAS:
        if capa not in presentes:
            inc.append((A, f"falta la capa {capa}: la arquitectura necesita al menos un componente en cada capa ({', '.join(DS.CAPAS)})"))
    for (c1, i1), (c2, i2) in zip(orden, orden[1:]):
        if i2 < i1:
            inc.append((A, f"{c2}: las capas van en orden ({' → '.join(DS.CAPAS)}); {c2} ({DS.CAPAS[i2]}) está después de {c1} ({DS.CAPAS[i1]})"))
            break
    if br is not None:
        brief_fue = {f["codigo"] for f in br["fuentes"]}
        en_fuentes = {x for c in comps if DS.capa_canonica(c["capa"]) == "Fuentes" for x in c["fuentes"]}
        for f in sorted(brief_fue - en_fuentes):
            inc.append((A, f"{f}: la fuente del brief no figura en la capa de fuentes"))
        for x in sorted({x for c in comps for x in c["fuentes"]} - brief_fue):
            inc.append((A, f"cita {x}, que no es una fuente del brief vigente"))
    inc += _repetidos([c["codigo"] for c in comps], A)
    if _vacio(d["flujo"]):
        inc.append((A, "falta el «**Flujo de los datos.**»"))
    return inc


def check_herramientas(d):
    A = "secciones/2.3.md"
    inc = []
    hs = d["herramientas"]
    if not hs:
        return [(A, "falta la tabla «Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada»")]
    capas = set()
    for h in hs:
        c, nombre = h["codigo"], h["herramienta"] or h["codigo"]
        capa = DS.capa_canonica(h["capa"])
        if capa is None:
            inc.append((A, f"{c}: capa «{h['capa']}» desconocida (usa {', '.join(DS.CAPAS)})"))
        else:
            capas.add(capa)
        if _vacio(h["herramienta"]):
            inc.append((A, f"{c}: falta el nombre de la herramienta (o «Pendiente» en ETL o almacenamiento)"))
            continue
        if _vacio(h["funcion"]):
            inc.append((A, f"{c} ({nombre}): falta su función en el proyecto"))
        if h["pendiente"]:
            if capa is not None and capa not in DS.CAPAS_PENDIENTE:
                inc.append((A, f"{c}: solo las herramientas de ETL y de almacenamiento pueden quedar «Pendiente»; la capa {capa} necesita su herramienta"))
            if _vacio(h["justificacion"]):
                inc.append((A, f"{c}: una herramienta «Pendiente» indica el motivo en la justificación («Pendiente: se decide con la construcción del capítulo 3»)"))
            continue
        if _vacio(h["justificacion"]) or D.pendiente(h["justificacion"].split(":")[0]):
            inc.append((A, f"{c} ({nombre}): falta la justificación de su elección"))
        if _vacio(h["alternativa"]):
            inc.append((A, f"{c} ({nombre}): falta la alternativa descartada"))
    for capa in ("ETL", "Almacenamiento", VISUALIZACION):
        if capa not in capas:
            inc.append((A, f"falta una herramienta de la capa {capa} (o «Pendiente» si aún no se decide y la capa lo admite)"))
    if not any(DS.capa_canonica(h["capa"]) == VISUALIZACION and "power bi" in h["herramienta"].lower() for h in hs):
        inc.append((A, "Power BI debe figurar en la capa de visualización (consigna del curso)"))
    inc += _repetidos([h["codigo"] for h in hs], A)
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = DS.leer_solucion(run)
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        br = None
        inc.append(("secciones/2.1.md", f"no se pueden comprobar los objetivos ni las fuentes sin el brief vigente: {e}"))
    try:
        principales = {c["codigo"] for c in D.leer(raiz, D.PROBLEMA)["principales"]}
    except (D.SinCorrida, P.ConfigError):
        principales = None  # sin corrida de 05 la propuesta se apoya en el brief y no se comprueban las causas
    return inc + check_propuesta(d, br, principales) + check_arquitectura(d, br) + check_herramientas(d)
