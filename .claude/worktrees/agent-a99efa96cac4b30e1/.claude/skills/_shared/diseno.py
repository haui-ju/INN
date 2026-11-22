#!/usr/bin/env python3
"""Capítulo 2 del informe (diseño técnico de la solución de BI): lectura de las secciones y modelo.json.

  python3 .claude/skills/_shared/diseno.py leer --paso 06-make-bi-solution [--run CORRIDA] [--raiz .]
  python3 .claude/skills/_shared/diseno.py leer --paso 07-make-data-model-kpi [--run CORRIDA] [--raiz .]
  python3 .claude/skills/_shared/diseno.py modelo --run RUTA_CORRIDA        (escribe <corrida>/modelo.json desde 2.4 y 2.5)

`06-make-bi-solution` escribe `secciones/2.1.md` a `2.3.md` (propuesta, arquitectura por capas y herramientas) y
`07-make-data-model-kpi` escribe `secciones/2.4.md` y `2.5.md` (modelo dimensional y KPI) con el mismo contrato que el
capítulo 1 (ver diagnostico.py). Este módulo lee esas secciones como datos para los validadores, los visuales y las
skills siguientes, y escribe `modelo.json` (el contrato con el capítulo 3) a partir de las secciones, que son la fuente
de verdad. Solo biblioteca estándar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import diagnostico as D  # noqa: E402
import projectcfg as P  # noqa: E402
import visuales as VI  # noqa: E402

SOLUCION, MODELO = "06-make-bi-solution", "07-make-data-model-kpi"
ARCHIVO_MODELO = "modelo.json"
CAPAS = ["Fuentes", "ETL", "Almacenamiento", "Visualización"]
CLAVE_CAPA = {"Fuentes": "fuentes", "ETL": "etl", "Almacenamiento": "almacenamiento", "Visualización": "visualizacion"}
CAPAS_PENDIENTE = ("ETL", "Almacenamiento")
CARDINALIDADES = ("N:1", "1:N", "1:1", "N:N")
FILTROS = ("Único", "Ambos")
AGREGACIONES = ("suma", "promedio", "conteo", "conteo distinto", "mínimo", "máximo")
PERIODICAS = ("Diaria", "Semanal", "Quincenal", "Mensual", "Trimestral", "Semestral", "Anual")
FRECUENCIAS = PERIODICAS + ("Por carga",)
RE_CAP, RE_HER, RE_FUE = re.compile(r"\bCAP-\d+\b"), re.compile(r"\bHER-\d+\b"), re.compile(r"\bFUE-\d+\b")
RE_OE = re.compile(r"\bOE-\d+\b")
RE_FCT, RE_DIM, RE_REL, RE_KPI = (re.compile(rf"^{p}-\d+$") for p in ("FCT", "DIM", "REL", "KPI"))
RE_CARD = re.compile(r"\b([1N]:[1N])\b")
RE_MEDIDA = re.compile(r"^([\w.]+)\s*\(([^,()]+),\s*([^()]+)\)$")
RE_CAMPO_DAX = re.compile(r"\b([A-Za-z_]\w*)\[([A-Za-z_]\w*)\]")
RE_TIEMPO = re.compile(r"fecha|tiempo|calendario", re.I)
SinCorrida = D.SinCorrida


def _filas(txt, *claves):
    t = VI.tabla(txt, *claves)
    return (t[0], t[1]) if t else (None, [])


def _lista(celda, sep=";"):
    c = (celda or "").strip()
    if c in ("", "—", "-", "–"):
        return []
    return [x.strip().rstrip(".").strip() for x in c.split(sep) if x.strip()]


def capa_canonica(t):
    """Nombre exacto de la capa (sin importar tildes ni mayúsculas) o None."""
    n = VI._norm(t or "")
    return next((c for c in CAPAS if VI._norm(c) == n), None)


# ------------------------------------------------------------------ 06: propuesta, arquitectura y herramientas
def leer_solucion(run):
    """Datos de 2.1 a 2.3 de una corrida de 06-make-bi-solution."""
    s21, s22, s23 = (D._seccion(run, p) for p in ("2.1", "2.2", "2.3"))
    pr_enc, pr = _filas(s21, "Objetivo", "Componentes")
    propuesta = [{"objetivo": f[0], "componentes": RE_CAP.findall(VI._col(pr_enc, f, "Componentes")),
                  "como": VI._col(pr_enc, f, "Como")} for f in pr if f and re.fullmatch(r"OE-\d+", f[0])]
    ca_enc, ca = _filas(s22, "Codigo", "Capa", "Componente")
    componentes = [{"codigo": f[0], "capa": VI._col(ca_enc, f, "Capa"), "componente": VI._col(ca_enc, f, "Componente"),
                    "funcion": VI._col(ca_enc, f, "Funcion"), "entrada": VI._col(ca_enc, f, "Entrada"),
                    "salida": VI._col(ca_enc, f, "Salida"), "fuentes": RE_FUE.findall(" ".join(f))}
                   for f in ca if f and RE_CAP.fullmatch(f[0])]
    he_enc, he = _filas(s23, "Codigo", "Herramienta", "Capa")
    herramientas = []
    for f in he:
        if not f or not RE_HER.fullmatch(f[0]):
            continue
        nombre = VI._col(he_enc, f, "Herramienta")
        herramientas.append({"codigo": f[0], "herramienta": nombre, "capa": VI._col(he_enc, f, "Capa"),
                             "funcion": VI._col(he_enc, f, "Funcion"), "justificacion": VI._col(he_enc, f, "Justificacion"),
                             "alternativa": VI._col(he_enc, f, "Alternativa"), "pendiente": D.pendiente(nombre)})
    return {"decisiones": D.vinetas(s21, "Decisiones que apoya"), "usuarios": VI.campo(s21, "Usuarios"),
            "respuesta": VI.campo(s21, "Respuesta a la problemática"), "causas": D.RE_CAU.findall(VI.campo(s21, "Respuesta a la problemática")),
            "propuesta": propuesta, "componentes": componentes, "flujo": VI.campo(s22, "Flujo de los datos"),
            "herramientas": herramientas}


# ------------------------------------------------------------------ 07: modelo y KPI
def _medidas(celda):
    out = []
    for x in _lista(celda):
        m = RE_MEDIDA.match(x)
        out.append({"nombre": m.group(1), "tipo": m.group(2).strip(), "agregacion": m.group(3).strip()} if m
                   else {"nombre": x, "tipo": "", "agregacion": ""})
    return out


def _jerarquias(celda):
    return [[n.strip() for n in j.split(">") if n.strip()] for j in _lista(celda)]


def _card(celda):
    m = RE_CARD.search((celda or "").upper())
    return m.group(1) if m else (celda or "").strip()


def leer_modelo(run):
    """Modelo y KPI de 2.4 y 2.5 de una corrida de 07-make-data-model-kpi, con el esquema de modelo.json."""
    s24, s25 = D._seccion(run, "2.4"), D._seccion(run, "2.5")
    h_enc, h = _filas(s24, "Codigo", "Tabla", "Granularidad")
    hechos = [{"codigo": f[0], "nombre": VI._col(h_enc, f, "Tabla"), "granularidad": VI._col(h_enc, f, "Granularidad"),
               "medidas": _medidas(VI._col(h_enc, f, "Medidas")), "claves": _lista(VI._col(h_enc, f, "Claves"))}
              for f in h if f and RE_FCT.match(f[0])]
    d_enc, d = _filas(s24, "Codigo", "Tabla", "Atributos")
    dims = [{"codigo": f[0], "nombre": VI._col(d_enc, f, "Tabla"), "clave": VI._col(d_enc, f, "Clave"),
             "atributos": _lista(VI._col(d_enc, f, "Atributos")), "jerarquias": _jerarquias(VI._col(d_enc, f, "Jerarquias"))}
            for f in d if f and RE_DIM.match(f[0])]
    r_enc, r = _filas(s24, "Codigo", "Desde", "Hacia")
    rels = [{"codigo": f[0], "desde": VI._col(r_enc, f, "Desde"), "hacia": VI._col(r_enc, f, "Hacia"),
             "campos": _lista(VI._col(r_enc, f, "Campos")), "cardinalidad": _card(VI._col(r_enc, f, "Cardinalidad")),
             "filtro": VI._col(r_enc, f, "Filtro")} for f in r if f and RE_REL.match(f[0])]
    k_enc, k = _filas(s25, "Codigo", "KPI", "Formula", "Origen")
    s_enc, s = _filas(s25, "Codigo", "Meta", "Frecuencia", "Objetivo")
    seg = {f[0]: f for f in s if f and RE_KPI.match(f[0])}
    kpis = []
    for f in k:
        if not f or not RE_KPI.match(f[0]):
            continue
        g = seg.get(f[0])
        kpis.append({"codigo": f[0], "nombre": VI._col(k_enc, f, "KPI"), "formula": VI._col(k_enc, f, "Formula"),
                     "medida": VI._col(k_enc, f, "Medida"), "origen": _lista(VI._col(k_enc, f, "Origen")),
                     "meta": VI._col(s_enc, g, "Meta") if g else "", "frecuencia": VI._col(s_enc, g, "Frecuencia") if g else "",
                     "objetivo": VI._col(s_enc, g, "Objetivo") if g else "", "decision": VI._col(s_enc, g, "Decision") if g else ""})
    return {"schema": 1, "hechos": hechos, "dimensiones": dims, "relaciones": rels, "kpis": kpis}


def seguimiento(run):
    """Códigos de la tabla de seguimiento de 2.5, en orden."""
    s_enc, s = _filas(D._seccion(run, "2.5"), "Codigo", "Meta", "Frecuencia", "Objetivo")
    return [f[0] for f in s if f and RE_KPI.match(f[0])]


def campos(modelo):
    """{tabla: set(campos)} del modelo: claves y medidas de los hechos; clave y atributos de las dimensiones."""
    out = {}
    for h in modelo["hechos"]:
        out[h["nombre"]] = set(h["claves"]) | {m["nombre"] for m in h["medidas"]}
    for d in modelo["dimensiones"]:
        out[d["nombre"]] = {d["clave"]} | set(d["atributos"])
    return out


def escribir_modelo(run):
    """Escribe <run>/modelo.json desde 2.4 y 2.5; devuelve el modelo."""
    m = leer_modelo(run)
    (Path(run) / ARCHIVO_MODELO).write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return m


def leer_json(run):
    """modelo.json de la corrida o None si no existe."""
    f = Path(run) / ARCHIVO_MODELO
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else None


LECTORES = {SOLUCION: leer_solucion, MODELO: leer_modelo}


def leer(raiz, paso, run=None):
    return LECTORES[paso](D.corrida(raiz, paso, run))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    le = sub.add_parser("leer")
    le.add_argument("--paso", required=True, choices=sorted(LECTORES))
    le.add_argument("--run")
    le.add_argument("--raiz", default=".")
    mo = sub.add_parser("modelo")
    mo.add_argument("--run", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "modelo":
            run = Path(a.run)
            if not run.is_dir():
                print(f"ERROR: {a.run} no es una carpeta", file=sys.stderr)
                return 2
            escribir_modelo(run)
            print(run / ARCHIVO_MODELO)
            return 0
        print(json.dumps(leer(Path(a.raiz).resolve(), a.paso, a.run), ensure_ascii=False, indent=2))
        return 0
    except (SinCorrida, P.ConfigError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
