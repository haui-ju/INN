#!/usr/bin/env python3
"""Brief del proyecto (paso 01-make-project-brief): lectura de sus secciones y copia de sus datos al config.

  python3 .claude/skills/_shared/brief.py leer      [--raiz .] [--run CORRIDA]     (datos del brief vigente en JSON)
  python3 .claude/skills/_shared/brief.py al-config [--raiz .] [--run CORRIDA]     (copia el tema y el calendario al config)

El brief (`project/01-project-brief/<corrida>/brief.md`) es la fuente del tema, la problemática, los objetivos, el alcance,
los usuarios y las decisiones, las fuentes de datos previstas y el calendario; las demás skills lo leen. Solo biblioteca estándar.
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

PASO = "01-make-project-brief"
CARPETA = "01-project-brief"
PENDIENTE = "Pendiente"
SECCIONES = ["1. Tema y empresa", "2. Problemática", "3. Objetivos", "4. Justificación y alcance", "5. Usuarios y decisiones",
             "6. Fuentes de datos previstas", "7. Calendario", "8. Supuestos y riesgos iniciales"]
TIPOS_INI = ("Supuesto", "Riesgo")
TIPOS_FUENTE = ("Interna", "Abierta", "Generada")
ACCESOS = ("Autorizado", "Público", "Pendiente")


class SinBrief(Exception):
    pass


def corrida(raiz, run=None):
    """Carpeta de la corrida del brief (la indicada o la vigente)."""
    nombre = run or P.current_run(PASO, raiz)
    if not nombre:
        raise SinBrief(f"no hay una corrida vigente de {PASO}")
    d = Path(raiz) / "project" / CARPETA / nombre
    if not (d / "brief.md").is_file():
        raise SinBrief(f"falta brief.md en la corrida {nombre}")
    return d


def _norm(t):
    return re.sub(r"\s+", " ", (t or "").strip())


def _filas(txt, *claves):
    t = VI.tabla(txt, *claves)
    return (t[0], t[1]) if t else (None, [])


def _objetivos(txt):
    enc, filas = _filas(txt, "Codigo", "Objetivo", "Meta")
    out = []
    for f in filas:
        if not f or not re.match(r"^O[GE]-\d+$", f[0]):
            continue
        out.append({"codigo": f[0], "objetivo": VI._col(enc, f, "Objetivo"), "metrica": VI._col(enc, f, "Metrica"), "meta": VI._col(enc, f, "Meta"),
                    "plazo": VI._col(enc, f, "Plazo"), "aporta": VI._col(enc, f, "Aporta"), "indicador": VI._col(enc, f, "Indicador")})
    return out


def _vinetas(txt, rotulo):
    m = re.search(r"\*\*" + re.escape(rotulo) + r"\.?\*\*\s*\n((?:\s*- .+\n?)+)", txt + "\n")
    return [_norm(x.strip()[2:]) for x in m.group(1).strip().splitlines()] if m else []


def _parrafos_justificacion(txt):
    """Párrafos del rótulo «**Justificación.**» (hasta el siguiente encabezado), sin el rótulo."""
    m = re.search(r"\*\*Justificación[.:]?\*\*\s*(.*?)(?=\n#{2,3}\s|\Z)", txt, re.S)
    if not m:
        return []
    return [_norm(p) for p in re.split(r"\n\s*\n", m.group(1).strip()) if _norm(p)]


def leer(txt):
    """Datos estructurados de un brief.md (los campos que no están salen vacíos)."""
    sec = VI.secciones(txt)

    def cuerpo(n):
        return next((v for k, v in sec.items() if k.startswith(f"{n}.")), "")
    obj = VI.secciones(cuerpo(3), 3)
    gen = next((v for k, v in obj.items() if k.startswith("3.1")), "")
    esp = next((v for k, v in obj.items() if k.startswith("3.2")), "")
    just = VI.secciones(cuerpo(4), 3)
    cal_enc, cal = _filas(cuerpo(7), "Inicio", "Entrega")
    fu_enc, fu = _filas(cuerpo(6), "Codigo", "Fuente", "Tipo")
    ini_enc, ini = _filas(cuerpo(8), "Codigo", "Tipo", "Descripcion")
    al_enc, al = _filas(next((v for k, v in just.items() if k.startswith("4.1")), ""), "Alcance", "Detalle")
    li_enc, li = _filas(next((v for k, v in just.items() if k.startswith("4.2")), ""), "Limitacion", "Detalle")
    m = re.search(r"(?m)^# Brief del proyecto\s*[·\-–]\s*(.+)$", txt)
    prob = cuerpo(2)
    tema_txt = re.sub(r"(?m)^#.*$", "", cuerpo(1))
    tema_txt = re.sub(r"(?m)^\*\*Empresa\.\*\*.*$", "", tema_txt)
    calendario = {"inicio": "", "entrega": ""}
    if cal:
        calendario = {"inicio": VI._col(cal_enc, cal[0], "Inicio"), "entrega": VI._col(cal_enc, cal[0], "Entrega")}
    return {
        "nombre": _norm(m.group(1)) if m else "",
        "secciones": [k for k in sec],
        "tema": _norm(tema_txt),
        "empresa": VI.campo(cuerpo(1), "Empresa"),
        "problematica": {"problema": VI.campo(prob, "Problema principal"), "afectados": VI.campo(prob, "Quién lo sufre"), "situacion": VI.campo(prob, "Situación actual"),
                         "evidencia": _vinetas(prob, "Evidencia")},
        "og": _objetivos(gen), "oe": _objetivos(esp),
        "justificacion": " ".join(_parrafos_justificacion(cuerpo(4))), "justificacion_parrafos": len(_parrafos_justificacion(cuerpo(4))),
        "alcance": [{"alcance": f[0], "detalle": f[1]} for f in al if len(f) >= 2], "limitaciones": [{"limitacion": f[0], "detalle": f[1]} for f in li if len(f) >= 2],
        "usuarios": VI.campo(cuerpo(5), "Usuarios"),
        "decisiones": _vinetas(cuerpo(5), "Decisiones que apoyará el dashboard"),
        "fuentes": [{"codigo": f[0], "fuente": VI._col(fu_enc, f, "Fuente"), "tipo": VI._col(fu_enc, f, "Tipo"), "datos": VI._col(fu_enc, f, "Datos"), "acceso": VI._col(fu_enc, f, "Acceso")}
                    for f in fu if f and re.match(r"^FUE-\d+$", f[0])],
        "calendario": calendario,
        "filas_calendario": len([f for f in cal if f]),
        "iniciales": [{"codigo": f[0], "tipo": VI._col(ini_enc, f, "Tipo"), "descripcion": VI._col(ini_enc, f, "Descripcion"), "vigilancia": VI._col(ini_enc, f, "vigila")} for f in ini if f and re.match(r"^INI-\d+$", f[0])],
    }


def vigente(raiz, run=None):
    """Datos del brief vigente (o de `run`); lanza SinBrief si no hay."""
    return leer((corrida(raiz, run) / "brief.md").read_text(encoding="utf-8"))


def _fecha_o_none(t):
    """DD-MM-AAAA -> texto si es una fecha válida; None si es «Pendiente» o vacío."""
    return t if P._fecha(t) is not None else None


def al_config(raiz, run=None):
    """Copia al config el tema y las fechas de inicio y entrega del brief."""
    d = vigente(raiz, run)
    return P.set_nucleo(d["tema"], inicio=_fecha_o_none(d["calendario"]["inicio"]), entrega=_fecha_o_none(d["calendario"]["entrega"]), root=raiz)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("leer", "al-config"):
        s = sub.add_parser(n)
        s.add_argument("--raiz", default=".")
        s.add_argument("--run")
    a = ap.parse_args(argv)
    raiz = Path(a.raiz).resolve()
    try:
        if a.cmd == "leer":
            print(json.dumps(vigente(raiz, a.run), ensure_ascii=False, indent=2))
        else:
            print(json.dumps(al_config(raiz, a.run), ensure_ascii=False))
        return 0
    except (SinBrief, P.ConfigError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
