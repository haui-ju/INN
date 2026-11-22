"""Reglas del paso 06-make-bi-solution (secciones 2.1 a 2.3; se invocan desde validate_run.py)."""
from pathlib import Path

import brief as BR
import diagnostico as D
import projectcfg as P

PASO = D.SOLUCION
PUNTOS = ["2.1", "2.2", "2.3"]
UPDATE = "06-make-bi-solution-update"
PREFIJOS = ("CAP", "HER")
CAPAS_PENDIENTES = ("ETL", "Almacenamiento")


def _vacio(t):
    return not (t or "").strip()


def check_propuesta(d, br, componentes):
    A = "secciones/2.1.md"
    inc = []
    if not d["decisiones"]:
        inc.append((A, "falta «**Decisiones que apoya.**» con al menos una viñeta"))
    if _vacio(d["usuarios"]):
        inc.append((A, "falta «**Usuarios.**»"))
    if _vacio(d["respuesta"]):
        inc.append((A, "falta «**Respuesta a la problemática.**»"))
    oe = {o["codigo"] for o in br["oe"]} if br else None
    filas = {f["objetivo"]: f for f in d["objetivos"]}
    if not d["objetivos"]:
        inc.append((A, "falta la tabla «Objetivo | Componentes | Cómo lo atiende»"))
    if oe is not None:
        for c in sorted(oe):
            if c not in filas:
                inc.append((A, f"{c}: el objetivo no aparece en la tabla de la propuesta"))
        for c in filas:
            if c not in oe:
                inc.append((A, f"{c} no es un objetivo específico del brief vigente"))
    for c, f in filas.items():
        if not f["componentes"]:
            inc.append((A, f"{c}: la fila no cita ningún componente (CAP-nn) de la arquitectura"))
        elif componentes is not None:
            for x in f["componentes"]:
                if x not in componentes:
                    inc.append((A, f"{c}: cita {x}, que no está en la tabla de 2.2"))
        if _vacio(f["como"]):
            inc.append((A, f"{c}: falta cómo lo atiende"))
    return inc


def check_arquitectura(d, br):
    A = "secciones/2.2.md"
    inc = []
    comp = d["componentes"]
    if not comp:
        return [(A, "falta la tabla «Código | Capa | Componente | Función | Entrada y salida»")]
    orden = []
    for c in comp:
        capa = next((n for n in D.CAPAS if D.norm(n) == D.norm(c["capa"])), None)
        if capa is None:
            inc.append((A, f"{c['codigo']}: la capa «{c['capa']}» no es una de {', '.join(D.CAPAS)}"))
            continue
        if capa not in orden:
            orden.append(capa)
        if _vacio(c["componente"]) or _vacio(c["funcion"]):
            inc.append((A, f"{c['codigo']}: falta el componente o su función"))
        if _vacio(c["entrada_salida"]):
            inc.append((A, f"{c['codigo']}: falta la entrada y salida"))
    for n in D.CAPAS:
        if n not in orden:
            inc.append((A, f"falta la capa de {n.lower()}: la tabla no tiene ningún componente de esa capa"))
    presentes = [n for n in D.CAPAS if n in orden]
    if orden != presentes:
        inc.append((A, f"las capas deben ir en el orden {', '.join(D.CAPAS)} (están en {', '.join(orden)})"))
    if _vacio(d["lectura"]):
        inc.append((A, "falta la «**Lectura de la arquitectura.**»"))
    if br is not None:
        texto_fuentes = " ".join(" ".join(str(v) for v in c.values()) for c in comp if D.norm(c["capa"]) == D.norm("Fuentes"))
        usadas = set(D.RE_FUE.findall(texto_fuentes))
        for f in br["fuentes"]:
            if f["codigo"] not in usadas:
                inc.append((A, f"{f['codigo']}: la fuente del brief no figura en la capa de fuentes"))
        validas = {f["codigo"] for f in br["fuentes"]}
        for x in sorted(usadas - validas):
            inc.append((A, f"cita {x}, que no es una fuente del brief vigente"))
    return inc


def check_herramientas(d):
    A = "secciones/2.3.md"
    inc = []
    her = d["herramientas"]
    if not her:
        return [(A, "falta la tabla «Código | Herramienta | Capa | Función en el proyecto | Justificación | Alternativa descartada»")]
    for h in her:
        capa = next((n for n in D.CAPAS if D.norm(n) == D.norm(h["capa"])), None)
        if capa is None:
            inc.append((A, f"{h['codigo']}: la capa «{h['capa']}» no es una de {', '.join(D.CAPAS)}"))
        if _vacio(h["herramienta"]):
            inc.append((A, f"{h['codigo']}: falta la herramienta (usa «Pendiente» solo en ETL o almacenamiento)"))
            continue
        nombre = h["herramienta"]
        if D.pendiente(nombre):
            if capa is not None and capa not in CAPAS_PENDIENTES:
                inc.append((A, f"{h['codigo']}: «Pendiente» solo se acepta en la capa de ETL o de almacenamiento"))
            if _vacio(h["justificacion"]):
                inc.append((A, f"{h['codigo']}: la herramienta pendiente necesita su motivo en la justificación"))
            continue
        if _vacio(h["justificacion"]):
            inc.append((A, f"{h['codigo']}: la herramienta «{nombre}» no tiene justificación"))
        if _vacio(h["alternativa"]):
            inc.append((A, f"{h['codigo']}: la herramienta «{nombre}» no tiene alternativa descartada"))
        if _vacio(h["funcion"]):
            inc.append((A, f"{h['codigo']}: la herramienta «{nombre}» no tiene función en el proyecto"))
    if not any("power bi" in D.norm(h["herramienta"]) and D.norm(h["capa"]) == D.norm("Visualización") for h in her):
        inc.append((A, "Power BI debe figurar como herramienta de la capa de visualización"))
    for n in D.CAPAS[1:]:
        if not any(D.norm(h["capa"]) == D.norm(n) for h in her):
            inc.append((A, f"ninguna herramienta (ni «Pendiente») para la capa de {n.lower()}"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = D.leer_solucion(run)
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        br = None
        inc.append(("secciones/2.1.md", f"no se pueden comprobar los objetivos y las fuentes sin el brief vigente: {e}"))
    componentes = {c["codigo"] for c in d["componentes"]}
    return (inc + check_propuesta(d, br, componentes) + check_arquitectura(d, br) + check_herramientas(d))
