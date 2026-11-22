"""Reglas del paso 03-make-business-diagnosis (secciones 1.1 a 1.4; se invocan desde validate_run.py)."""
import re
from pathlib import Path

import diagnostico as D
import projectcfg as P

PASO = D.NEGOCIO
PUNTOS = ["1.1", "1.2", "1.3", "1.4"]
UPDATE = "03-make-business-diagnosis-update"
FILAS_EMPRESA = ["Razón social", "Nombre comercial", "RUC", "Actividad económica", "Ubicación"]
ASPECTOS = ["Sector", "Actividad económica (CIIU)", "Tipo de cliente", "Entorno competitivo"]
DATOS_TAMANO = ["Ventas anuales", "UIT de referencia", "Ventas en UIT", "Categoría (Ley 30056)"]
CATEGORIAS = [(150, "Microempresa"), (1700, "Pequeña empresa"), (2300, "Mediana empresa"), (float("inf"), "Gran empresa")]


def _vacio(t):
    return not (t or "").strip()


def _fila(tabla, nombre):
    """Valor de la fila `nombre` (sin tildes ni mayúsculas); None si no está."""
    n = D.norm(nombre)
    for k, v in tabla.items():
        if D.norm(k) == n:
            return v
    return None


def categoria(uit):
    return next(c for tope, c in CATEGORIAS if uit <= tope)


def check_empresa(d, cfg, dom):
    A = "secciones/1.1.md"
    inc = []
    for fila in FILAS_EMPRESA:
        v = _fila(d["empresa"], fila)
        if v is None:
            inc.append((A, f"falta la fila «{fila}» en la tabla «Dato | Valor»"))
        elif _vacio(v):
            inc.append((A, f"la fila «{fila}» está vacía"))
    ruc = _fila(d["empresa"], "RUC") or ""
    if cfg["proyecto"]["tipo"] == "empresa":
        if re.sub(r"\D", "", ruc) != str(cfg["proyecto"].get("ruc") or ""):
            inc.append((A, f"el RUC ({ruc}) no coincide con el del config ({cfg['proyecto'].get('ruc')})"))
    elif ruc and not D.norm(ruc).startswith("no aplica"):
        inc.append((A, "con tipo: propio el RUC debe decir «No aplica (empresa planteada por el equipo)»"))
    nombre = _fila(d["empresa"], "Nombre comercial")
    esperado = dom["datos"].get("Nombre comercial")
    if nombre and esperado and not D.pendiente(esperado) and "..." not in esperado and D.norm(nombre) != D.norm(esperado):
        inc.append((A, f"el nombre comercial ({nombre}) difiere del de domain.md ({esperado})"))
    if _vacio(d["resena"]):
        inc.append((A, "falta la «**Reseña.**»"))
    return inc


def check_mision(d, dom):
    A = "secciones/1.2.md"
    inc = []
    for rot, clave in (("Misión", "mision"), ("Visión", "vision")):
        v = d[clave]
        if _vacio(v) or D.pendiente(v):
            inc.append((A, f"falta la «**{rot}.**» (la rúbrica la exige)"))
            continue
        esperado = dom["secciones"].get(rot, "")
        if esperado and not D.pendiente(esperado) and "..." not in esperado and D.norm(v) != D.norm(esperado):
            inc.append((A, f"la {rot.lower()} difiere de la de domain.md: se copia sin cambios (o se corrige primero domain.md)"))
    if _vacio(d["relacion"]):
        inc.append((A, "falta la «**Relación con el proyecto.**»"))
    return inc


def check_tamano(d):
    A = "secciones/1.3.md"
    inc = []
    for a in ASPECTOS:
        v = _fila(d["industria"], a)
        if v is None or _vacio(v):
            inc.append((A, f"falta el aspecto «{a}» en la tabla «Aspecto | Descripción»"))
    t = d["tamano"]
    for k in DATOS_TAMANO:
        if _fila(t, k) is None:
            inc.append((A, f"falta el dato «{k}» en la tabla «Dato | Valor» del tamaño"))
    if inc:
        return inc
    cat = _fila(t, "Categoría (Ley 30056)")
    nombres = [c for _, c in CATEGORIAS]
    cat_ok = next((c for c in nombres if D.norm(c) == D.norm(cat)), None)
    if cat_ok is None:
        return [(A, f"la categoría «{cat}» debe ser {', '.join(nombres)}")]
    ventas, uit, en_uit = (_fila(t, k) for k in ("Ventas anuales", "UIT de referencia", "Ventas en UIT"))
    if D.pendiente(ventas) or D.pendiente(en_uit):
        return inc
    v, u, e = D.numero(ventas), D.numero(uit), D.numero(en_uit)
    if None in (v, u, e) or u == 0:
        return [(A, "ventas anuales, UIT y ventas en UIT deben ser cifras (o «Pendiente» en ventas y ventas en UIT)")]
    calc = v / u
    if abs(calc - e) > 1:
        inc.append((A, f"ventas en UIT: {ventas} ÷ {uit} = {calc:.0f}, no {en_uit}"))
    if categoria(calc) != cat_ok:
        inc.append((A, f"con {calc:.0f} UIT la categoría según la Ley 30056 es «{categoria(calc)}», no «{cat_ok}»"))
    return inc


def check_canvas(d):
    A = "secciones/1.4.md"
    inc = []
    por = {D.norm(b["bloque"]): b for b in d["canvas"]}
    for b in D.BLOQUES_BMC:
        x = por.get(D.norm(b))
        if x is None:
            inc.append((A, f"falta el bloque «{b}» en la tabla «Bloque | Contenido»"))
        elif not x["items"]:
            inc.append((A, f"el bloque «{b}» está vacío"))
    extra = [b["bloque"] for b in d["canvas"] if D.norm(b["bloque"]) not in {D.norm(x) for x in D.BLOQUES_BMC}]
    for b in extra:
        inc.append((A, f"bloque desconocido «{b}» (usa los nueve nombres exactos del Canvas)"))
    if _vacio(d["lectura"]):
        inc.append((A, "falta la «**Lectura del modelo.**» que relaciona el Canvas con la problemática"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_comunes(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    d = D.leer_negocio(run)
    try:
        cfg = P.load(raiz)
    except P.ConfigError as e:
        return inc + [("secciones/1.1.md", f"no se puede comprobar contra el config: {e}")]
    dom = D.dominio(raiz)
    return inc + check_empresa(d, cfg, dom) + check_mision(d, dom) + check_tamano(d) + check_canvas(d)
