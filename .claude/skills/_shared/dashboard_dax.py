"""DAX propuesto para los KPI del modelo (puro: recibe `modelo.json` ya cargado, no ejecuta nada).

Es un borrador para que el equipo lo pruebe en Power BI: una medida base por cada campo de un hecho que usan los KPI (con la agregación que
declara el modelo) y una medida por KPI armada con la fórmula en palabras de 2.5. Lo que no puede relacionar con un campo del modelo queda
marcado con `/* revisar: … */` y listado en `revisar`. La medida que cuenta es la que el equipo ejecutó (anexo C).

  python3 .claude/skills/_shared/dashboard_dax.py MODELO.json     (imprime las medidas propuestas)
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

FUNCION = {"suma": "SUM", "promedio": "AVERAGE", "conteo": "COUNT", "conteo distinto": "DISTINCTCOUNT", "mínimo": "MIN", "máximo": "MAX"}
ETIQUETA = {"suma": "Suma de", "promedio": "Promedio de", "conteo": "Conteo de", "conteo distinto": "Conteo distinto de", "mínimo": "Mínimo de", "máximo": "Máximo de"}
# Referencias DAX: Tabla[campo] o 'Tabla'[campo] (campo de una tabla) y [Medida] sin tabla (otra medida).
RE_CAMPO = re.compile(r"(?:'([^']+)'|\b([A-Za-z_][A-Za-z0-9_]*))\[([^\]]+)\]")
RE_MEDIDA = re.compile(r"(?<![\w'\]])\[([^\]]+)\]")


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t or "") if not unicodedata.combining(c))


def norm(t):
    return re.sub(r"\s+", " ", sin_tildes(t).lower()).strip()


def tablas_campos(modelo):
    """{tabla: {campos}}: medidas y claves de los hechos; clave y atributos de las dimensiones."""
    out = {}
    for h in modelo.get("hechos", []):
        out[h["nombre"]] = {m["nombre"] for m in h.get("medidas", [])} | set(h.get("claves", []))
    for d in modelo.get("dimensiones", []):
        out[d["nombre"]] = {d["clave"], *d.get("atributos", [])}
    return out


def agregaciones(modelo):
    """{(tabla, campo): agregación} de las medidas de los hechos."""
    return {(h["nombre"], m["nombre"]): m.get("agregacion", "suma") for h in modelo.get("hechos", []) for m in h.get("medidas", [])}


def nombre_base(tabla, campo, agregacion):
    return f"{ETIQUETA.get(agregacion, 'Suma de')} {campo}"


def campos_citados(dax):
    """[(tabla, campo)] que cita un DAX con la forma Tabla[campo] o 'Tabla'[campo]."""
    return [(m.group(1) or m.group(2), m.group(3)) for m in RE_CAMPO.finditer(dax or "")]


def medidas_citadas(dax):
    """Nombres de las medidas citadas sin tabla ([Medida])."""
    return [m.group(1) for m in RE_MEDIDA.finditer(dax or "")]


def problemas_dax(dax, modelo, medidas_definidas=()):
    """Causas (vacío si está bien) de un DAX: tablas o campos que no están en el modelo y medidas que no están definidas."""
    tablas = tablas_campos(modelo)
    definidas = {norm(m) for m in medidas_definidas}
    out = []
    for t, c in campos_citados(dax):
        if t not in tablas:
            out.append(f"cita la tabla «{t}», que no está en modelo.json")
        elif c not in tablas[t]:
            out.append(f"cita el campo «{t}[{c}]», que no está en modelo.json")
    for m in medidas_citadas(dax):
        if norm(m) not in definidas:
            out.append(f"cita la medida «[{m}]», que no está definida en el anexo")
    return out


def _palabras(t):
    return {p[:-1] if len(p) > 4 and p.endswith("s") else p for p in re.findall(r"[a-z0-9]+", norm(t)) if p not in ("de", "del", "la", "el", "los", "las", "por", "en")}


def _termino(texto, candidatos):
    """Campo (tabla, campo) que mejor describe un término; None si no hay uno solo."""
    pt = _palabras(texto)
    puntaje = sorted(((len(pt & _palabras(c.replace("_", " "))), (t, c)) for t, c in candidatos), reverse=True)
    if not puntaje or puntaje[0][0] == 0 or (len(puntaje) > 1 and puntaje[1][0] == puntaje[0][0]):
        return None
    return puntaje[0][1]


def _lado(texto, candidatos, agreg, base, revisar):
    """Expresión DAX de un lado de la fórmula (términos separados por «menos» o «más»)."""
    t = re.sub(r"[()]", "", texto)
    t = re.split(r",| por | en el periodo| del periodo", t)[0]
    partes = re.split(r"\s+(menos|más|mas)\s+", t.strip())
    expr, signo = "", ""
    for i, p in enumerate(partes):
        if p in ("menos", "más", "mas"):
            signo = " - " if p == "menos" else " + "
            continue
        p = re.sub(r"^(promedio|suma|total|conteo)\s+(de(?:l)?\s+)?", "", p.strip(), flags=re.I)
        campo = _termino(p, candidatos)
        if campo:
            ref = f"[{base[campo]}]"
        else:
            ref = f"/* revisar: {p.strip()} */ BLANK()"
            revisar.append(p.strip())
        expr += (signo if expr else "") + ref
        signo = ""
    return expr


def medidas_base(modelo, kpis=None):
    """[{nombre, dax, tabla, campo}]: una medida base por cada campo de un hecho que usan los KPI (con su agregación)."""
    agreg = agregaciones(modelo)
    usados = []
    for k in kpis if kpis is not None else modelo.get("kpis", []):
        for o in k.get("origen", []):
            t, _, c = o.partition(".")
            if (t, c) in agreg and (t, c) not in usados:
                usados.append((t, c))
    return [{"nombre": nombre_base(t, c, agreg[(t, c)]), "tabla": t, "campo": c,
             "dax": f"{FUNCION.get(agreg[(t, c)], 'SUM')}({t}[{c}])"} for t, c in usados]


def medida_kpi(kpi, modelo):
    """{nombre, dax, revisar} del KPI. `revisar` lista los términos de la fórmula que no se pudieron relacionar con un campo."""
    agreg = agregaciones(modelo)
    origen = [tuple(o.partition(".")[::2]) for o in kpi.get("origen", [])]
    hechos = {t for t, _ in origen if any(t == h["nombre"] for h in modelo.get("hechos", []))}
    candidatos = [(t, c) for (t, c) in agreg if t in hechos]
    base = {k: nombre_base(k[0], k[1], v) for k, v in agreg.items()}
    revisar = []
    formula = kpi.get("formula", "")
    if " entre " in formula:
        num, den = formula.split(" entre ", 1)
        n, d = _lado(num, candidatos, agreg, base, revisar), _lado(den, candidatos, agreg, base, revisar)
        cuerpo = f"DIVIDE({n}, {d})"
        if n == d:
            # Falta un filtro (CALCULATE sobre un atributo de una dimensión) o una medida que el modelo no relaciona con el texto.
            revisar.append("el numerador y el denominador salen iguales: falta un filtro o la medida del denominador")
            cuerpo = f"/* revisar: numerador y denominador iguales */ {cuerpo}"
    else:
        cuerpo = _lado(formula, candidatos, agreg, base, revisar)
    return {"nombre": kpi["medida"], "dax": f"// Fórmula: {formula}\n{cuerpo}", "revisar": revisar}


def proponer(modelo):
    """[{codigo, nombre, kpi, dax, revisar}] con las medidas base y las de cada KPI, numeradas MED-01 en adelante (primero las base)."""
    out = [{"nombre": b["nombre"], "kpi": "", "dax": b["dax"], "revisar": [], "tablas": [b["tabla"]]} for b in medidas_base(modelo)]
    for k in modelo.get("kpis", []):
        m = medida_kpi(k, modelo)
        out.append({"nombre": m["nombre"], "kpi": k["codigo"], "dax": m["dax"], "revisar": m["revisar"], "tablas": []})
    for i, m in enumerate(out, 1):
        m["codigo"] = f"MED-{i:02d}"
    return out


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    if len(a) != 1:
        print(__doc__)
        return 1
    modelo = json.loads(Path(a[0]).read_text(encoding="utf-8"))
    for m in proponer(modelo):
        print(f"{m['codigo']} · {m['nombre']}" + (f" ({m['kpi']})" if m["kpi"] else ""))
        print(m["dax"])
        if m["revisar"]:
            print(f"  ¡revisar!: {'; '.join(m['revisar'])}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
