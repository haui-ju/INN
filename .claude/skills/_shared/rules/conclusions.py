#!/usr/bin/env python3
"""Reglas del paso 11-make-conclusions (sección 5; se invocan desde validate_run.py) y cálculo del estado de cada objetivo.

  python3 .claude/skills/_shared/rules/conclusions.py estados [--raiz .] [--json]
      (estado calculado de cada KPI, de cada objetivo específico y del general, con el valor real y la meta)

El estado de una conclusión no se opina: sale del valor real de `valores.json` (09-make-dashboard) frente a la meta de 2.5
(modelo.json), según el sentido del indicador. La regla está en common/11-conclusions/guia.md, punto 1.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import brief as BR  # noqa: E402
import diagnostico as D  # noqa: E402
import projectcfg as P  # noqa: E402
import visuales as VI  # noqa: E402
from rules import dashboard as DB  # noqa: E402

PASO = "11-make-conclusions"
PUNTOS = ["5"]
UPDATE = "11-make-conclusions-update"
PREFIJOS = ("CNC", "REC", "LEC")
ESTADOS = ("Cumplido", "Parcial", "No cumplido", "Sin meta")
ESTADOS_KPI = ("Cumple", "No cumple", "Sin meta")
S = "secciones/5.md"
STORYTELLING = "10-make-storytelling"
DASHBOARD = "09-make-dashboard"
RE_PENDIENTE = re.compile(r"pendiente|no se puede|no es posible|sin meta|no hay meta|no tiene meta", re.I)


def _vacio(t):
    return not (t or "").strip()


# ------------------------------------------------------------------ cálculo del estado
def estado_kpi(meta_texto, valor):
    """«Cumple», «No cumple» o «Sin meta»; None si hay meta y falta el valor."""
    if _vacio(meta_texto) or D.pendiente(meta_texto):
        return "Sin meta"
    meta = D.numero(meta_texto)
    if meta is None:
        return "Sin meta"
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        return None
    cmp = DB._comparador(meta_texto) or ">="          # una cifra sin sentido («100 %») se alcanza con ese valor o más
    return "Cumple" if (valor >= meta if cmp == ">=" else valor <= meta) else "No cumple"


def estado_objetivo(estados):
    """Estado de un objetivo específico a partir del estado de sus KPI (guía, punto 1b)."""
    con_meta = [e for e in estados if e != "Sin meta"]
    if not con_meta:
        return "Sin meta"
    cumplen = [e for e in con_meta if e == "Cumple"]
    if len(cumplen) == len(estados):
        return "Cumplido"
    return "No cumplido" if not cumplen else "Parcial"


def estado_general(estados):
    """Estado del objetivo general a partir de los de los específicos (guía, punto 1c)."""
    if estados and all(e == "Cumplido" for e in estados):
        return "Cumplido"
    if estados and all(e == "No cumplido" for e in estados):
        return "No cumplido"
    if estados and all(e == "Sin meta" for e in estados):
        return "Sin meta"
    return "Parcial"


def evaluar(br, modelo, valores):
    """({OE: {codigo, objetivo, kpis, estado}}, {OG: {...}}) con el estado calculado; el estado es None si falta un valor."""
    vals = {x.get("codigo"): x for x in (valores or {}).get("kpis", [])}
    especificos = []
    for oe in br["oe"]:
        kpis = []
        for k in modelo.get("kpis", []):
            if k.get("objetivo") != oe["codigo"]:
                continue
            v = vals.get(k["codigo"])
            valor = v.get("valor") if v else None
            kpis.append({"codigo": k["codigo"], "nombre": k.get("nombre", ""), "meta": k.get("meta", ""), "valor": valor,
                         "unidad": (v or {}).get("unidad", ""), "estado": estado_kpi(k.get("meta", ""), valor) if v else None})
        estados = [x["estado"] for x in kpis]
        estado = None if (None in estados) else estado_objetivo(estados) if estados else "Sin meta"
        especificos.append({"codigo": oe["codigo"], "objetivo": oe["objetivo"], "kpis": kpis, "estado": estado})
    generales = []
    est_oe = [x["estado"] for x in especificos]
    for og in br["og"]:
        generales.append({"codigo": og["codigo"], "objetivo": og["objetivo"], "estado": None if None in est_oe else estado_general(est_oe)})
    return especificos, generales


# ------------------------------------------------------------------ fuentes
def _json(f):
    if not f.is_file():
        return None, None
    try:
        return json.loads(f.read_text(encoding="utf-8")), None
    except ValueError as e:
        return None, str(e)


def cargar(raiz):
    """{br, modelo, valores, problemas}: las fuentes vigentes y lo que no se pudo leer (lista de textos)."""
    raiz = Path(raiz)
    out = {"br": None, "modelo": None, "valores": None, "problemas": []}
    try:
        out["br"] = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        out["problemas"].append(f"no se pueden comprobar los objetivos sin el brief vigente: {e}")
    try:
        out["modelo"], err = _json(D.corrida(raiz, D.MODELO) / "modelo.json")
        if out["modelo"] is None:
            out["problemas"].append("no se pueden comprobar los KPI sin el modelo.json de 07-make-data-model-kpi" + (f" ({err})" if err else ""))
    except D.SinCorrida as e:
        out["problemas"].append(f"no se pueden comprobar los KPI sin la corrida de 07-make-data-model-kpi: {e}")
    try:
        d9 = D.corrida(raiz, DASHBOARD)
        out["valores"], err = _json(d9 / "valores.json")
        if out["valores"] is None:
            out["problemas"].append(f"falta valores.json en la corrida vigente de {DASHBOARD}: sin los valores reales del equipo no se puede concluir" + (f" ({err})" if err else ""))
    except D.SinCorrida as e:
        out["problemas"].append(f"falta la corrida vigente de {DASHBOARD} (valores.json): sin los valores reales del equipo no se puede concluir ({e})")
    return out


# ------------------------------------------------------------------ lectura de la sección
def conclusiones(txt):
    """[{codigo, objetivo, estado, texto}] de la tabla de conclusiones."""
    t = VI.tabla(txt, "Codigo", "Objetivo", "Estado", "Conclusion")
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "objetivo": (re.findall(r"O[GE]-\d+", VI._col(enc, f, "Objetivo")) or [""])[0], "estado": VI._col(enc, f, "Estado").strip(),
             "texto": VI._col(enc, f, "Conclusion")} for f in filas if f and re.fullmatch(r"CNC-\d+", f[0])]


def respaldo(txt):
    """[{cnc, kpi, valor, meta, estado}] de la tabla de respaldo."""
    t = VI.tabla(txt, "Conclusion", "KPI", "Valor", "Meta")
    if not t:
        return []
    enc, filas = t
    return [{"cnc": f[0], "kpi": VI._col(enc, f, "KPI"), "valor": VI._col(enc, f, "Valor"), "meta": VI._col(enc, f, "Meta"),
             "estado": VI._col(enc, f, "Estado")} for f in filas if f and re.fullmatch(r"CNC-\d+", f[0])]


def recomendaciones(txt):
    """[{codigo, cnc, texto, decide, kpi}] de la tabla de recomendaciones."""
    t = VI.tabla(txt, "Codigo", "Conclusion", "Recomendacion", "Decide")
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "cnc": (re.findall(r"CNC-\d+", VI._col(enc, f, "Conclusion")) or [""])[0], "texto": VI._col(enc, f, "Recomendacion"),
             "decide": VI._col(enc, f, "Decide"), "kpi": VI._col(enc, f, "KPI")} for f in filas if f and re.fullmatch(r"REC-\d+", f[0])]


def lecciones(txt):
    t = VI.tabla(txt, "Codigo", "Leccion")
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "texto": VI._col(enc, f, "Leccion")} for f in filas if f and re.fullmatch(r"LEC-\d+", f[0])]


# ------------------------------------------------------------------ comprobaciones
def _detalle(kpis):
    return "; ".join(f"{k['codigo']} {k['valor']} frente a «{k['meta']}» = {k['estado']}" for k in kpis) or "sin KPI"


def check_conclusiones(conc, especificos, generales):
    inc = []
    if not conc:
        return [(S, "falta la tabla de conclusiones «Código | Objetivo | Estado | Conclusión»")]
    por_obj = {}
    for c in conc:
        por_obj.setdefault(c["objetivo"], []).append(c)
    esperados = {x["codigo"]: x for x in especificos + generales}
    for c in conc:
        if c["objetivo"] not in esperados:
            inc.append((S, f"{c['codigo']}: el objetivo «{c['objetivo']}» no es uno del brief"))
        if _vacio(c["texto"]):
            inc.append((S, f"{c['codigo']}: falta la conclusión"))
    for codigo, x in esperados.items():
        filas = por_obj.get(codigo, [])
        if not filas:
            inc.append((S, f"{codigo}: el objetivo no tiene conclusión (CNC-nn)"))
            continue
        if len(filas) > 1:
            inc.append((S, f"{codigo}: tiene más de una conclusión ({', '.join(f['codigo'] for f in filas)}): una por objetivo"))
        c = filas[0]
        if c["estado"] not in ESTADOS:
            inc.append((S, f"{c['codigo']}: el estado debe ser uno de {', '.join(ESTADOS)}"))
        elif x["estado"] is not None and c["estado"] != x["estado"]:
            det = _detalle(x.get("kpis", [])) if "kpis" in x else "estados de los objetivos específicos"
            inc.append((S, f"{c['codigo']}: el estado «{c['estado']}» no concuerda con el valor real frente a la meta: debe ser «{x['estado']}» ({det})"))
    cnc_oe = {c["objetivo"]: c["codigo"] for c in conc if c["objetivo"].startswith("OE-")}
    for g in generales:
        cg = next((c for c in conc if c["objetivo"] == g["codigo"]), None)
        if cg:
            for oe, cod in cnc_oe.items():
                if cod not in cg["texto"]:
                    inc.append((S, f"{cg['codigo']}: la conclusión del objetivo general debe citar {cod} ({oe})"))
    return inc


def check_respaldo(conc, resp, especificos, valores):
    inc = []
    if not resp:
        return [(S, "falta la tabla de respaldo «Conclusión | KPI | Valor real | Meta | Estado del KPI»")]
    vals = {x.get("codigo"): x for x in (valores or {}).get("kpis", [])}
    cnc_de = {c["objetivo"]: c["codigo"] for c in conc}
    por_cnc = {}
    for r in resp:
        por_cnc.setdefault(r["cnc"], []).append(r)
    codigos = {c["codigo"] for c in conc}
    for r in resp:
        if r["cnc"] not in codigos:
            inc.append((S, f"{r['cnc']}: la tabla de respaldo cita una conclusión que no está definida"))
    for oe in especificos:
        cnc = cnc_de.get(oe["codigo"])
        if not cnc:
            continue
        filas = {r["kpi"]: r for r in por_cnc.get(cnc, [])}
        for k in oe["kpis"]:
            r = filas.get(k["codigo"])
            if r is None:
                inc.append((S, f"{cnc}: falta en el respaldo el KPI {k['codigo']}, que mide {oe['codigo']}"))
                continue
            v = vals.get(k["codigo"])
            if v is not None:
                real, citado = v.get("valor"), D.numero(r["valor"])
                if not isinstance(real, (int, float)) or isinstance(real, bool):
                    pass
                elif citado is None or abs(citado - real) > 0.5 * 10 ** -DB._decimales(r["valor"]) + 1e-9:
                    inc.append((S, f"{cnc}: el valor de {k['codigo']} «{r['valor']}» no coincide con valores.json ({real})"))
            if DB._norm(r["meta"]) != DB._norm(k["meta"]):
                inc.append((S, f"{cnc}: la meta de {k['codigo']} «{r['meta']}» no es la de modelo.json («{k['meta']}»)"))
            if r["estado"] not in ESTADOS_KPI:
                inc.append((S, f"{cnc}: el estado de {k['codigo']} debe ser uno de {', '.join(ESTADOS_KPI)}"))
            elif k["estado"] is not None and r["estado"] != k["estado"]:
                inc.append((S, f"{cnc}: el estado de {k['codigo']} «{r['estado']}» no concuerda con {k['valor']} frente a «{k['meta']}»: debe ser «{k['estado']}»"))
        propios = {k["codigo"] for k in oe["kpis"]}
        for kpi in filas:
            if kpi not in propios:
                inc.append((S, f"{cnc}: el respaldo cita {kpi}, que no mide {oe['codigo']} en modelo.json"))
    return inc


def check_meta_pendiente(conc, especificos):
    """Si algún KPI del objetivo no tiene meta, su conclusión dice que no se puede concluir el cumplimiento."""
    inc = []
    cnc_de = {c["objetivo"]: c for c in conc}
    for oe in especificos:
        sin = [k["codigo"] for k in oe["kpis"] if k["estado"] == "Sin meta"]
        c = cnc_de.get(oe["codigo"])
        if sin and c and not RE_PENDIENTE.search(c["texto"]):
            inc.append((S, f"{c['codigo']}: {', '.join(sin)} no tiene meta; la conclusión debe decir que su cumplimiento no se puede concluir porque la meta está pendiente"))
    return inc


def check_recomendaciones(txt, conc, recs, br, modelo):
    inc = []
    if not recs:
        return [(S, "falta la tabla de recomendaciones «Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará»")]
    roles = DB._roles(br["usuarios"]) if br else None
    kpis = {k["codigo"] for k in (modelo or {}).get("kpis", [])}
    cnc_ok = {c["codigo"]: c for c in conc}
    for r in recs:
        c = r["codigo"]
        if not r["cnc"]:
            inc.append((S, f"{c}: la recomendación no cita ninguna conclusión (CNC-nn)"))
        elif r["cnc"] not in cnc_ok:
            inc.append((S, f"{c}: cita {r['cnc']}, que no es una conclusión definida"))
        if _vacio(r["texto"]):
            inc.append((S, f"{c}: falta la acción recomendada"))
        if _vacio(r["decide"]):
            inc.append((S, f"{c}: no indica quién decide"))
        elif roles is not None and not any(x in DB._norm(r["decide"]) or DB._norm(r["decide"]) in x for x in roles):
            inc.append((S, f"{c}: «{r['decide']}» no es un usuario del brief ({br['usuarios']})"))
        ks = re.findall(r"KPI-\d+", r["kpi"])
        if not ks:
            inc.append((S, f"{c}: no indica el KPI que mostrará si funcionó"))
        for k in ks:
            if modelo is not None and k not in kpis:
                inc.append((S, f"{c}: cita {k}, que no es un KPI de modelo.json"))
    con_rec = {r["cnc"] for r in recs}
    for c in conc:
        if c["estado"] in ESTADOS and c["estado"] != "Cumplido" and c["codigo"] not in con_rec:
            inc.append((S, f"{c['codigo']}: la conclusión es «{c['estado']}» y no tiene ninguna recomendación (REC-nn)"))
    return inc


def check_lecciones_y_limitaciones(txt, lecs, modo):
    inc = []
    if not lecs:
        inc.append((S, "falta la tabla de lecciones aprendidas «Código | Lección | Dónde se vio» con al menos una LEC-nn"))
    for l in lecs:
        if _vacio(l["texto"]):
            inc.append((S, f"{l['codigo']}: falta la lección"))
    lim = VI.campo(txt, "Limitaciones")
    if _vacio(lim):
        inc.append((S, "falta el párrafo «**Limitaciones.**»"))
    elif modo == "generado" and not re.search(r"gener", lim, re.I):
        inc.append((S, "con modo_datos «generado», «Limitaciones» debe decir que los datos se generaron para el proyecto"))
    return inc


def check_hallazgos(raiz, txt):
    """Los HLZ-nn que cita la sección existen en la sección 4 de la corrida vigente de 10 (si hay)."""
    citados = set(re.findall(r"HLZ-\d+", txt))
    if not citados:
        return []
    try:
        t4 = D.texto(D.corrida(raiz, STORYTELLING), "4")
    except (D.SinCorrida, OSError, KeyError):
        return [(S, f"cita {', '.join(sorted(citados))} y no hay corrida vigente de {STORYTELLING}")]
    conocidos = set(re.findall(r"HLZ-\d+", t4 or ""))
    return [(S, f"{h}: el hallazgo no está en la sección 4 de {STORYTELLING}") for h in sorted(citados - conocidos)]


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    txt = D.texto(run, "5")
    for n in DB._tablas_sin_titulo(txt):
        inc.append((S, f"línea {n}: la tabla no tiene su título «Tabla N: …» justo antes"))
    f = cargar(raiz)
    for p in f["problemas"]:
        inc.append((S, p))
    if f["br"] is None or f["modelo"] is None or f["valores"] is None:
        return inc
    try:
        modo = P.load(raiz).get("modo_datos")
    except P.ConfigError:
        modo = None
    especificos, generales = evaluar(f["br"], f["modelo"], f["valores"])
    for x in especificos:
        for k in x["kpis"]:
            if k["estado"] is None:
                inc.append(("valores.json", f"{k['codigo']}: falta su valor real en valores.json (mide {x['codigo']})"))
    conc, resp, recs, lecs = conclusiones(txt), respaldo(txt), recomendaciones(txt), lecciones(txt)
    inc += check_conclusiones(conc, especificos, generales) + check_respaldo(conc, resp, especificos, f["valores"])
    inc += check_meta_pendiente(conc, especificos) + check_recomendaciones(txt, conc, recs, f["br"], f["modelo"])
    inc += check_lecciones_y_limitaciones(txt, lecs, modo) + check_hallazgos(raiz, txt)
    return inc


# ------------------------------------------------------------------ línea de comandos
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("estados")
    e.add_argument("--raiz", default=".")
    e.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    f = cargar(a.raiz)
    for p in f["problemas"]:
        print(f"AVISO: {p}", file=sys.stderr)
    if f["br"] is None or f["modelo"] is None or f["valores"] is None:
        return 1
    especificos, generales = evaluar(f["br"], f["modelo"], f["valores"])
    if a.json:
        print(json.dumps({"especificos": especificos, "generales": generales}, ensure_ascii=False, indent=2))
        return 0
    for x in especificos:
        print(f"{x['codigo']}  {x['estado']}  ·  {x['objetivo']}")
        for k in x["kpis"]:
            print(f"    {k['codigo']}  {k['valor']} {k['unidad']}  frente a «{k['meta']}»  →  {k['estado']}  ({k['nombre']})")
    for g in generales:
        print(f"{g['codigo']}  {g['estado']}  ·  {g['objetivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
