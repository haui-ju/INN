"""Reglas específicas del paso 01-make-project-brief (se invocan desde validate_run.py)."""
import re
from pathlib import Path

import brief as BR
import projectcfg as P
import visuales as VI

NIVEL3 = {"3": ("3.1", "3.2"), "4": ("4.1", "4.2")}
UPDATE = "01-make-project-brief-update"


def _pend(t):
    return (t or "").strip().lower() == BR.PENDIENTE.lower()


def _vacio(t):
    return not (t or "").strip()


def _plazo(t):
    """Fecha citada en «Entrega (DD-MM-AAAA)»; «Pendiente» si es «Entrega (Pendiente)»; None si no tiene el formato."""
    m = re.fullmatch(r"Entrega \((\d{2}-\d{2}-\d{4}|Pendiente)\)", (t or "").strip())
    return m.group(1) if m else None


def check_secciones(txt, d):
    A = "brief.md"
    inc = []
    if not re.search(r"(?m)^# Brief del proyecto\s*[·\-–]\s*\S", txt):
        inc.append((A, "falta el título «# Brief del proyecto · <nombre>»"))
    titulos = list(d["secciones"])
    for esperado in BR.SECCIONES:
        if esperado not in titulos:
            inc.append((A, f"falta el encabezado «## {esperado}»"))
    presentes = [t for t in BR.SECCIONES if t in titulos]
    if [t for t in titulos if t in BR.SECCIONES] != presentes:
        inc.append((A, "las secciones no están en el orden del brief"))
    for n, (a, b) in NIVEL3.items():
        sec = next((k for k in titulos if k.startswith(f"{n}.")), None)
        if sec is None:
            continue
        cuerpo = VI.secciones(txt)[sec]
        subs = list(VI.secciones(cuerpo, 3))
        for p in (a, b):
            if not any(s.startswith(p) for s in subs):
                inc.append((A, f"falta el encabezado «### {p}.» en la sección {n}"))
    return inc


def check_contenido(d):
    A = "brief.md"
    inc = []
    for nombre, valor in (("Tema", d["tema"]), ("Empresa", d["empresa"]), ("Problema principal", d["problematica"]["problema"]),
                          ("Quién lo sufre", d["problematica"]["afectados"]), ("Situación actual", d["problematica"]["situacion"]),
                          ("Usuarios", d["usuarios"])):
        if _vacio(valor):
            inc.append((A, f"«{nombre}» está vacío (escribe el contenido o «{BR.PENDIENTE}»)"))
    if not d["problematica"]["evidencia"]:
        inc.append((A, "la problemática no tiene «Evidencia.» (usa una viñeta con «Pendiente» si aún no hay)"))
    if not d["decisiones"]:
        inc.append((A, "faltan las «Decisiones que apoyará el dashboard» (al menos una viñeta, o «Pendiente»)"))
    if _vacio(d["justificacion"]):
        inc.append((A, "falta la «**Justificación.**» (uno o dos párrafos: qué decisión mejora, qué impacto tiene y por qué una solución de BI)"))
    elif d["justificacion_parrafos"] > 2:
        inc.append((A, f"la justificación tiene {d['justificacion_parrafos']} párrafos; debe ser uno o dos"))
    for nombre, filas in (("alcance", d["alcance"]), ("limitaciones", d["limitaciones"])):
        if not filas:
            inc.append((A, f"falta la tabla de {nombre}"))
    if d["alcance"] and not {f["alcance"] for f in d["alcance"]} >= {"Incluye", "No incluye"}:
        inc.append((A, "la tabla de alcance necesita las filas «Incluye» y «No incluye»"))
    return inc


def check_fuentes(d):
    A = "brief.md"
    if not d["fuentes"]:
        return [(A, "no hay fuentes de datos previstas FUE-nn (usa una fila con «Pendiente» si aún no se conocen)")]
    inc = []
    for f in d["fuentes"]:
        if _vacio(f["fuente"]) or _vacio(f["datos"]):
            inc.append((A, f"{f['codigo']}: faltan la fuente o los datos"))
        if f["tipo"] not in BR.TIPOS_FUENTE and not _pend(f["tipo"]):
            inc.append((A, f"{f['codigo']}: el tipo debe ser {', '.join(BR.TIPOS_FUENTE)}"))
        if f["acceso"] not in BR.ACCESOS:
            inc.append((A, f"{f['codigo']}: el acceso debe ser {', '.join(BR.ACCESOS)}"))
    return inc


def check_calendario(d):
    A = "brief.md"
    if d["filas_calendario"] != 1:
        return [(A, "el calendario debe tener una sola fila con «Inicio» y «Entrega»")]
    inc = []
    c = d["calendario"]
    i, e = P._fecha(c["inicio"]), P._fecha(c["entrega"])
    for k, v, f in (("Inicio", c["inicio"], i), ("Entrega", c["entrega"], e)):
        if f is None and not _pend(v):
            inc.append((A, f"{k}: «{v}» no es una fecha DD-MM-AAAA válida ni «{BR.PENDIENTE}»"))
    if i and e and e < i:
        inc.append((A, f"la entrega ({c['entrega']}) es anterior al inicio ({c['inicio']})"))
    return inc


def check_objetivos(d):
    A = "brief.md"
    inc = []
    og, oe = d["og"], d["oe"]
    if len(og) != 1 or og[0]["codigo"] != "OG-01":
        inc.append((A, "debe haber exactamente un objetivo general OG-01"))
    if len(oe) < 2:
        inc.append((A, "debe haber al menos dos objetivos específicos OE-nn"))
    entrega = d["calendario"]["entrega"]
    vistos = set()
    for o in og + oe:
        c = o["codigo"]
        if c in vistos:
            inc.append((A, f"{c}: código repetido"))
        vistos.add(c)
        for campo in ("objetivo", "metrica", "meta", "plazo", "indicador"):
            if _vacio(o[campo]):
                inc.append((A, f"{c}: falta {'el ' if campo in ('objetivo', 'indicador') else 'la '}{campo}"))
        if c.startswith("OE") and o["aporta"] != "OG-01":
            inc.append((A, f"{c}: «Aporta a» debe ser OG-01"))
        if not _vacio(o["plazo"]) and not _pend(o["plazo"]):
            p = _plazo(o["plazo"])
            if p is None:
                inc.append((A, f"{c}: el plazo debe ser «Entrega (DD-MM-AAAA)»"))
            elif p != BR.PENDIENTE and not _pend(entrega) and p != entrega:
                inc.append((A, f"{c}: el plazo cita {p} y la entrega del calendario es {entrega}"))
    return inc


def check_iniciales(d):
    A = "brief.md"
    inc = []
    if not d["iniciales"]:
        return [(A, "no hay supuestos ni riesgos iniciales INI-nn")]
    for f in d["iniciales"]:
        if f["tipo"] not in BR.TIPOS_INI:
            inc.append((A, f"{f['codigo']}: el tipo debe ser {' o '.join(BR.TIPOS_INI)}"))
        if _vacio(f["descripcion"]):
            inc.append((A, f"{f['codigo']}: falta la descripción"))
    return inc


def check_config(d, cfg):
    A = "brief.md"
    inc = []
    if cfg["proyecto"]["tema"] != d["tema"]:
        inc.append((A, f"el tema del config ({cfg['proyecto']['tema']!r}) difiere del de la sección 1 ({d['tema']!r}); copie el brief con brief.py al-config o use {UPDATE}"))
    for k in ("inicio", "entrega"):
        v = d["calendario"][k]
        esperado = None if _pend(v) else v
        if cfg["calendario"].get(k) != esperado:
            inc.append((A, f"calendario.{k} del config ({cfg['calendario'].get(k)}) difiere del calendario del brief ({v})"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    f = run / "brief.md"
    if not f.exists():
        return [("brief.md", "falta el archivo")]
    txt = f.read_text(encoding="utf-8")
    d = BR.leer(txt)
    inc = check_secciones(txt, d)
    if inc and any("falta el encabezado" in m for _, m in inc):
        return inc
    inc += check_contenido(d) + check_fuentes(d) + check_calendario(d) + check_objetivos(d) + check_iniciales(d)
    try:
        cfg = P.load(raiz)
    except P.ConfigError as e:
        return inc + [("brief.md", f"no se puede comprobar contra el config: {e}")]
    inc += check_config(d, cfg)
    if not (raiz / cfg["dominio"]).is_file():
        inc.append((cfg["dominio"], "falta domain.md: la skill lo crea después de confirmar el brief"))
    return inc
