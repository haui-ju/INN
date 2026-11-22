"""Reglas del paso 04-make-strategic-analysis (secciones 1.5 a 1.7; se invocan desde validate_run.py)."""
import re
from collections import Counter
from pathlib import Path

import brief as BR
import diagnostico as D
import projectcfg as P
import visuales as VI

PASO = D.ESTRATEGICO
PUNTOS = ["1.5", "1.6", "1.7"]
UPDATE = "04-make-strategic-analysis-update"
PREFIJOS = ("POL", "ECO", "SOC", "TEC", "AMB", "LEG", "FOR", "DEB", "OPO", "AME", "FO", "FA", "DO", "DA", "CAU")
MIN_CAUSAS, MIN_CATEGORIAS = 6, 4
RE_ANIO = re.compile(r"\b(?:19|20)\d{2}\b")


def _vacio(t):
    return not (t or "").strip()


def _repetidos(codigos, archivo):
    return [(archivo, f"código repetido: {c}") for c, n in Counter(codigos).items() if n > 1]


def check_pestel(d, txt):
    A = "secciones/1.5.md"
    inc = []
    if not d["pestel"]:
        return [(A, "falta la tabla «Código | Factor | Hallazgo | Efecto en el negocio | Tipo | Fuente»")]
    for pref, factor in D.FACTORES.items():
        if not any(i["codigo"].startswith(pref + "-") for i in d["pestel"]):
            inc.append((A, f"falta al menos un hallazgo del factor {factor} ({pref}-nn)"))
    for i in d["pestel"]:
        c = i["codigo"]
        esperado = D.FACTORES[c.split("-")[0]]
        if D.norm(i["factor"]) != D.norm(esperado):
            inc.append((A, f"{c}: el factor debe ser «{esperado}» (según su prefijo)"))
        for campo, nombre in (("hallazgo", "el hallazgo"), ("efecto", "el efecto en el negocio")):
            if _vacio(i[campo]):
                inc.append((A, f"{c}: falta {nombre}"))
        if i["tipo"] not in D.TIPOS_PESTEL:
            inc.append((A, f"{c}: el tipo debe ser {' o '.join(D.TIPOS_PESTEL)}"))
        if _vacio(i["fuente"]):
            inc.append((A, f"{c}: falta la fuente"))
        elif not RE_ANIO.search(i["fuente"]):
            inc.append((A, f"{c}: la fuente debe llevar su año"))
    inc += _repetidos([i["codigo"] for i in d["pestel"]], A)
    if _vacio(VI.campo(txt, "Síntesis")):
        inc.append((A, "falta la «**Síntesis.**» del PESTEL"))
    return inc


def check_foda(d):
    A = "secciones/1.6.md"
    inc = []
    pestel = {i["codigo"] for i in d["pestel"]}
    for pref, clave in D.CUADRANTES.items():
        items = d["foda"][clave]
        if not items:
            inc.append((A, f"falta la tabla «Código | {D.NOMBRE_CUADRANTE[pref]} | Evidencia o fuente» con al menos un ítem {pref}-nn"))
        for i in items:
            if _vacio(i["texto"]):
                inc.append((A, f"{i['codigo']}: falta el texto"))
            if _vacio(i["evidencia"]):
                inc.append((A, f"{i['codigo']}: falta la evidencia o fuente"))
            elif pref in ("OPO", "AME"):
                cita = D.RE_PESTEL.findall(i["evidencia"])
                if not cita and not RE_ANIO.search(i["evidencia"]):
                    inc.append((A, f"{i['codigo']}: la evidencia debe citar un hallazgo PESTEL (POL, ECO, SOC, TEC, AMB, LEG) o una fuente con su año"))
                for c in cita:
                    if c not in pestel:
                        inc.append((A, f"{i['codigo']}: cita {c}, que no está en el PESTEL"))
    inc += _repetidos([i["codigo"] for v in d["foda"].values() for i in v], A)
    return inc


def check_estrategias(d):
    A = "secciones/1.6.md"
    inc = []
    foda = {i["codigo"] for v in d["foda"].values() for i in v}
    if not d["estrategias"]:
        return [(A, "falta la tabla de estrategias cruzadas «Código | Tipo | Estrategia | Combina»")]
    for tipo in D.ESTRATEGIAS:
        if not any(e["codigo"].startswith(tipo + "-") for e in d["estrategias"]):
            inc.append((A, f"falta al menos una estrategia {tipo} ({tipo}-nn)"))
    for e in d["estrategias"]:
        c, tipo = e["codigo"], e["codigo"].split("-")[0]
        if e["tipo"] != tipo:
            inc.append((A, f"{c}: el tipo debe ser {tipo} (según su prefijo)"))
        if _vacio(e["texto"]):
            inc.append((A, f"{c}: falta la estrategia"))
        interno, externo = D.ESTRATEGIAS[tipo]
        prefs = {x.split("-")[0] for x in e["combina"]}
        if interno not in prefs or externo not in prefs or prefs - {interno, externo}:
            nombres = {"FOR": "fortalezas", "DEB": "debilidades", "OPO": "oportunidades", "AME": "amenazas"}
            inc.append((A, f"{c}: una estrategia {tipo} combina {nombres[interno]} con {nombres[externo]} (cita al menos un {interno} y un {externo}, y nada más)"))
        for x in e["combina"]:
            if x not in foda:
                inc.append((A, f"{c}: combina {x}, que no está en la matriz FODA"))
    inc += _repetidos([e["codigo"] for e in d["estrategias"]], A)
    return inc


def check_ishikawa(d, txt, problema):
    A = "secciones/1.7.md"
    inc = []
    if _vacio(d["efecto"]):
        inc.append((A, "falta el «**Efecto.**» (el problema principal del brief)"))
    elif problema is not None and D.norm(d["efecto"]) != D.norm(problema):
        inc.append((A, f"el efecto no coincide con el problema principal del brief («{problema}»): cópialo sin cambios o cambia el brief con 01-make-project-brief-update"))
    if not d["causas"]:
        return inc + [(A, "falta la tabla «Código | Categoría | Causa | Evidencia»")]
    validas = {D.norm(c) for c in D.CATEGORIAS_6M}
    for x in d["causas"]:
        c = x["codigo"]
        if D.norm(x["categoria"]) not in validas:
            inc.append((A, f"{c}: categoría «{x['categoria']}» desconocida (usa {', '.join(D.CATEGORIAS_6M)})"))
        if _vacio(x["causa"]):
            inc.append((A, f"{c}: falta la causa"))
        if _vacio(x["evidencia"]):
            inc.append((A, f"{c}: falta la evidencia"))
    foda = {i["codigo"] for v in d["foda"].values() for i in v}
    for x in d["causas"]:
        for cod in D.RE_FODA.findall(x["evidencia"]):
            if cod not in foda:
                inc.append((A, f"{x['codigo']}: cita {cod}, que no está en la matriz FODA"))
    if len(d["causas"]) < MIN_CAUSAS:
        inc.append((A, f"hay {len(d['causas'])} causas; el Ishikawa necesita al menos {MIN_CAUSAS}"))
    cats = {D.norm(x["categoria"]) for x in d["causas"]} & validas
    if len(cats) < MIN_CATEGORIAS:
        inc.append((A, f"las causas cubren {len(cats)} categorías; se necesitan al menos {MIN_CATEGORIAS} de las 6M"))
    inc += _repetidos([x["codigo"] for x in d["causas"]], A)
    if _vacio(VI.campo(txt, "Lectura del diagrama")):
        inc.append((A, "falta la «**Lectura del diagrama.**»"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = D.leer_estrategico(run)
    try:
        problema = BR.vigente(raiz)["problematica"]["problema"]
    except (BR.SinBrief, P.ConfigError) as e:
        problema = None
        inc.append(("secciones/1.7.md", f"no se puede comparar el efecto con el brief: {e}"))
    return (inc + check_pestel(d, D.texto(run, "1.5")) + check_foda(d) + check_estrategias(d)
            + check_ishikawa(d, D.texto(run, "1.7"), problema))
