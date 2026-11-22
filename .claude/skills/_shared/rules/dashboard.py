"""Reglas del paso 09-make-dashboard (sección 3.2, anexos C y D, valores.json y capturas; se invocan desde validate_run.py)."""
import json
import re
from pathlib import Path

import brief as BR
import dashboard_dax as DAX
import diagnostico as D
import projectcfg as P
import visuales as VI

PASO = "09-make-dashboard"
PUNTOS = ["3.2"]
ANEXOS = ("C", "D")
UPDATE = "09-make-dashboard-update"
PREFIJOS = ("PAG", "MED")
ESTADOS = ("Cumple", "No cumple", "Sin meta")
RE_CAPTURA = re.compile(r"^<!--\s*captura:\s*([a-z0-9][\w-]*)\s*-->$")
RE_TITULO_TABLA = re.compile(r"^Tabla \d+:\s*\S")
S = "secciones/3.2.md"


def _vacio(t):
    return not (t or "").strip()


def _norm(t):
    return DAX.norm(D.norm(t))


# ------------------------------------------------------------------ lectura
def titulo_anexo(letra):
    """«Anexo C: Medidas…»: el título del índice sin los paréntesis finales."""
    for ln in D.INDICE.read_text(encoding="utf-8").splitlines():
        m = re.match(rf"^- Anexo {letra}: (.+)$", ln)
        if m:
            t = m.group(1).strip()
            while True:
                n = re.sub(r"\s*\([^()]*\)\s*$", "", t)
                if n == t:
                    return t
                t = n
    return ""


def _fenced(lineas):
    """Índices de las líneas que están dentro de un bloque de código."""
    dentro, out = False, set()
    for i, l in enumerate(lineas):
        if l.strip().startswith("```"):
            dentro = not dentro
            out.add(i)
            continue
        if dentro:
            out.add(i)
    return out


def paginas(txt):
    """[{codigo, pagina, pregunta, usuario, visualizaciones, filtros, kpis}] de la tabla de páginas de 3.2."""
    t = VI.tabla(txt, "Codigo", "Pagina", "Pregunta", "Usuario")
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "pagina": VI._col(enc, f, "Pagina"), "pregunta": VI._col(enc, f, "Pregunta"), "usuario": VI._col(enc, f, "Usuario"),
             "visualizaciones": VI._col(enc, f, "Visualizaciones"), "filtros": VI._col(enc, f, "Filtros"),
             "kpis": re.findall(r"KPI-\d+", VI._col(enc, f, "KPI"))} for f in filas if f and re.fullmatch(r"PAG-\d+", f[0])]


def kpis_32(txt):
    """[{codigo, nombre, valor, meta, estado, pagina}] de la tabla de valores reales de 3.2."""
    t = VI.tabla(txt, "Codigo", "KPI", "Valor", "Meta", "Estado")
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "nombre": VI._col(enc, f, "KPI"), "valor": VI._col(enc, f, "Valor"), "meta": VI._col(enc, f, "Meta"),
             "estado": VI._col(enc, f, "Estado"), "pagina": VI._col(enc, f, "Pagina")} for f in filas if f and re.fullmatch(r"KPI-\d+", f[0])]


def capturas_marcadas(txt):
    return [m.group(1) for ln in txt.splitlines() if (m := RE_CAPTURA.match(ln.strip()))]


def medidas_anexo(txt):
    """{codigo: {nombre, dax}} de los encabezados «### MED-nn. Nombre» y su primer bloque de código."""
    lin = txt.splitlines()
    dentro = _fenced(lin)
    cab = [(i, m) for i, l in enumerate(lin) if i not in dentro and (m := re.match(r"^#{3,}\s+(MED-\d+)\.\s+(.+?)\s*$", l))]
    out = {}
    for n, (i, m) in enumerate(cab):
        fin = cab[n + 1][0] if n + 1 < len(cab) else len(lin)
        bloque, abierto = [], False
        for l in lin[i + 1:fin]:
            if l.strip().startswith("```"):
                if abierto:
                    break
                abierto = True
                continue
            if abierto:
                bloque.append(l)
        out[m.group(1)] = {"nombre": m.group(2).strip(), "dax": "\n".join(bloque).strip()}
    return out


def paginas_anexo(txt):
    """{codigo: descripción} de los encabezados «### PAG-nn. Página» del anexo D."""
    lin = txt.splitlines()
    dentro = _fenced(lin)
    cab = [(i, m.group(1)) for i, l in enumerate(lin) if i not in dentro and (m := re.match(r"^#{3,}\s+(PAG-\d+)\.\s+.+$", l))]
    out = {}
    for n, (i, c) in enumerate(cab):
        fin = cab[n + 1][0] if n + 1 < len(cab) else len(lin)
        out[c] = VI.campo("\n".join(lin[i + 1:fin]), "Descripción")
    return out


def _tablas_sin_titulo(txt):
    lin = txt.splitlines()
    dentro = _fenced(lin)
    out = []
    for i, l in enumerate(lin):
        if i in dentro or not l.strip().startswith("|") or (i > 0 and lin[i - 1].strip().startswith("|")):
            continue
        previa = next((x for x in reversed(lin[:i]) if x.strip()), "")
        if not RE_TITULO_TABLA.match(previa.strip()):
            out.append(i + 1)
    return out


def _texto(run, rel):
    f = Path(run) / rel
    return f.read_text(encoding="utf-8") if f.is_file() else None


def _json(f):
    if not f.is_file():
        return None, None
    try:
        return json.loads(f.read_text(encoding="utf-8")), None
    except ValueError as e:
        return None, str(e)


# ------------------------------------------------------------------ comprobaciones
def _roles(usuarios):
    """Roles del brief («Gerente general (decide) y jefe de cocina (…)») normalizados."""
    t = re.sub(r"\([^)]*\)", "", usuarios or "")
    return [r for r in (_norm(x) for x in re.split(r",|;|\sy\s|\se\s", t)) if r]


def check_paginas(pags, modelo, br):
    inc = []
    if not pags:
        return [(S, "falta la tabla de páginas «Código | Página | Pregunta de negocio | Usuario | Visualizaciones | Filtros | KPI»")]
    roles = _roles(br["usuarios"]) if br else None
    cubiertos = set()
    for p in pags:
        c = p["codigo"]
        for rot, clave in (("el nombre de la página", "pagina"), ("su pregunta de negocio", "pregunta"), ("sus visualizaciones", "visualizaciones"), ("sus filtros", "filtros")):
            if _vacio(p[clave]):
                inc.append((S, f"{c}: falta {rot}"))
        if _vacio(p["usuario"]):
            inc.append((S, f"{c}: no indica qué usuario del brief la consulta"))
        elif roles is not None and not any(r in _norm(p["usuario"]) or _norm(p["usuario"]) in r for r in roles):
            inc.append((S, f"{c}: el usuario «{p['usuario']}» no es uno de los del brief ({br['usuarios']})"))
        if not p["kpis"]:
            inc.append((S, f"{c}: no muestra ningún KPI"))
        for k in p["kpis"]:
            if modelo is not None and k not in {x["codigo"] for x in modelo.get("kpis", [])}:
                inc.append((S, f"{c}: cita {k}, que no es un KPI de modelo.json"))
        cubiertos.update(p["kpis"])
    if modelo is not None:
        for k in modelo.get("kpis", []):
            if k["codigo"] not in cubiertos:
                inc.append((S, f"{k['codigo']}: el KPI no aparece en ninguna página"))
    return inc


def _comparador(meta):
    m = _norm(meta)
    if re.search(r"o mas|como minimo", m):
        return ">="
    if re.search(r"o menos|como maximo", m):
        return "<="
    return None


def _decimales(texto):
    m = re.search(r"\d[\d  .,]*[.,](\d+)(?!\d)", texto or "")
    return len(m.group(1)) if m else 0


def check_valores(filas, pags, modelo, valores, run):
    inc = []
    J = "valores.json"
    if not filas:
        return [(S, "falta la tabla de valores «Código | KPI | Valor real | Meta | Estado | Página»")]
    por_codigo = {f["codigo"]: f for f in filas}
    kpis = {k["codigo"]: k for k in modelo.get("kpis", [])} if modelo else {}
    vals = {x.get("codigo"): x for x in (valores or {}).get("kpis", [])}
    for c in kpis:
        if c not in por_codigo:
            inc.append((S, f"{c}: el KPI no tiene fila en la tabla de valores reales"))
    for f in filas:
        c = f["codigo"]
        k = kpis.get(c)
        if modelo is not None and k is None:
            inc.append((S, f"{c}: no es un KPI de modelo.json"))
            continue
        v = vals.get(c)
        if valores is not None and v is None:
            inc.append((J, f"{c}: el valor real de 3.2 no está en valores.json"))
            continue
        if v is not None:
            real, citado = v.get("valor"), D.numero(f["valor"])
            if not isinstance(real, (int, float)) or isinstance(real, bool):
                inc.append((J, f"{c}: el valor debe ser un número"))
            elif citado is None or abs(citado - real) > 0.5 * 10 ** -_decimales(f["valor"]) + 1e-9:
                inc.append((S, f"{c}: el valor real citado «{f['valor']}» no coincide con valores.json ({real})"))
        if f["estado"] not in ESTADOS:
            inc.append((S, f"{c}: el estado debe ser uno de {', '.join(ESTADOS)}"))
        if k is not None:
            meta_md = k.get("meta", "")
            pend = D.pendiente(meta_md)
            if _norm(f["meta"]) != _norm(meta_md):
                inc.append((S, f"{c}: la meta «{f['meta']}» no es la de modelo.json («{meta_md}»)"))
            if pend:
                if f["estado"] != "Sin meta":
                    inc.append((S, f"{c}: no tiene meta, su estado debe ser «Sin meta»"))
                if v is not None and v.get("meta") is not None:
                    inc.append((J, f"{c}: valores.json trae una meta y 2.5 sigue «Pendiente»: ciérrala con 07-make-data-model-kpi-update y vuelve a armar"))
            else:
                meta_n = D.numero(meta_md)
                if v is not None and v.get("meta") is None:
                    inc.append((J, f"{c}: la meta de 2.5 («{meta_md}») no está en valores.json"))
                elif v is not None and meta_n is not None and abs(v["meta"] - meta_n) > 1e-9:
                    inc.append((J, f"{c}: la meta de valores.json ({v['meta']}) no es la de 2.5 ({meta_n})"))
                cmp = _comparador(meta_md)
                real = (v or {}).get("valor")
                if cmp and meta_n is not None and isinstance(real, (int, float)) and f["estado"] in ("Cumple", "No cumple"):
                    ok = real >= meta_n if cmp == ">=" else real <= meta_n
                    if ok != (f["estado"] == "Cumple"):
                        inc.append((S, f"{c}: el estado «{f['estado']}» no concuerda con el valor {real} frente a la meta «{meta_md}»"))
                elif f["estado"] == "Sin meta":
                    inc.append((S, f"{c}: tiene meta «{meta_md}» y el estado es «Sin meta»"))
        pg = f["pagina"]
        pagina = next((p for p in pags if p["codigo"] == pg), None)
        if pagina is None:
            inc.append((S, f"{c}: la página «{pg}» no está en la tabla de páginas"))
        elif c not in pagina["kpis"]:
            inc.append((S, f"{c}: la página {pg} no lista este KPI"))
        elif not (Path(run) / "capturas" / f"{pg.lower()}.png").is_file():
            inc.append((S, f"{c}: cita un valor que muestra {pg} y falta su captura (capturas/{pg.lower()}.png)"))
    return inc


def check_capturas(txt, pags, run):
    inc = []
    marcadas = capturas_marcadas(txt)
    esperadas = [p["codigo"].lower() for p in pags]
    for i in esperadas:
        if marcadas.count(i) != 1:
            inc.append((S, f"debe marcar una sola vez la captura de la página con la línea «<!-- captura: {i} -->»"))
        png = Path(run) / "capturas" / f"{i}.png"
        if not png.is_file() or png.stat().st_size == 0:
            inc.append((f"capturas/{i}.png", f"falta la captura de la página {i.upper()} (la entrega el equipo)"))
    for m in marcadas:
        if m not in esperadas:
            inc.append((S, f"la captura «{m}» no corresponde a ninguna página de la tabla"))
    return inc


def check_texto(txt, valores_json, modelo):
    inc = []
    if _vacio(VI.campo(txt, "Lectura del dashboard")):
        inc.append((S, "falta la «**Lectura del dashboard.**»"))
    sin_meta = [k["codigo"] for k in (modelo or {}).get("kpis", []) if D.pendiente(k.get("meta", ""))]
    if sin_meta:
        parrafo = VI.campo(txt, "Metas pendientes")
        faltan = [c for c in sin_meta if c not in parrafo]
        if faltan:
            inc.append((S, f"falta la «**Metas pendientes.**» con {', '.join(faltan)} y la skill que las cierra ({UPDATE.replace('09-make-dashboard', '07-make-data-model-kpi')})"))
    comentarios = [ln for ln in txt.splitlines() if "<!--" in ln and not RE_CAPTURA.match(ln.strip())]
    if comentarios:
        inc.append((S, f"comentario que no es una marca de captura: «{comentarios[0].strip()[:60]}» (el texto es final, sin notas)"))
    n = _tablas_sin_titulo(txt)
    if n:
        inc.append((S, f"la tabla de la línea {n[0]} no tiene título «Tabla N: …»"))
    return inc


def check_anexo_c(run, modelo):
    A = "anexos/C.md"
    txt = _texto(run, A)
    if txt is None:
        return [(A, "falta el archivo (anexo C: medidas y cálculos del dashboard)")]
    inc = []
    esperado = f"# Anexo C: {titulo_anexo('C')}"
    primera = next((ln.strip() for ln in txt.splitlines() if ln.strip()), "")
    if primera != esperado:
        inc.append((A, f"la primera línea debe ser «{esperado}» (está «{primera[:80]}»)"))
    n = _tablas_sin_titulo(txt)
    if n:
        inc.append((A, f"la tabla de la línea {n[0]} no tiene título «Tabla N: …»"))
    meds = medidas_anexo(txt)
    if not meds:
        return inc + [(A, "no define ninguna medida «### MED-nn. Nombre» con su bloque ```dax")]
    nombres = [m["nombre"] for m in meds.values()]
    for c, m in meds.items():
        if _vacio(m["dax"]):
            inc.append((A, f"{c}: la medida «{m['nombre']}» no tiene su código DAX en un bloque ```dax"))
            continue
        if "revisar" in m["dax"].lower():
            inc.append((A, f"{c}: el DAX conserva una marca «revisar» sin resolver (el anexo lleva la medida final del equipo)"))
        if modelo is not None:
            for causa in DAX.problemas_dax(m["dax"], modelo, nombres):
                inc.append((A, f"{c}: la medida «{m['nombre']}» {causa}"))
    if modelo is not None:
        for k in modelo.get("kpis", []):
            if _norm(k["medida"]) not in {_norm(x) for x in nombres}:
                inc.append((A, f"{k['codigo']}: el anexo no define su medida «{k['medida']}»"))
    t = VI.tabla(txt, "Codigo", "Medida", "Tipo")
    if t:
        enc, filas = t
        en_tabla = {f[0] for f in filas if f and re.fullmatch(r"MED-\d+", f[0])}
        for c in sorted(en_tabla - set(meds)):
            inc.append((A, f"{c}: está en la tabla de medidas y no tiene su «### {c}. Nombre» con el DAX"))
        for c in sorted(set(meds) - en_tabla):
            inc.append((A, f"{c}: tiene su DAX y falta en la tabla de medidas"))
    else:
        inc.append((A, "falta la tabla «Código | Medida | Tipo | KPI | Tablas y campos»"))
    return inc


def check_anexo_d(run, pags):
    A = "anexos/D.md"
    txt = _texto(run, A)
    if txt is None:
        return [(A, "falta el archivo (anexo D: especificación y capturas del dashboard)")]
    inc = []
    esperado = f"# Anexo D: {titulo_anexo('D')}"
    primera = next((ln.strip() for ln in txt.splitlines() if ln.strip()), "")
    if primera != esperado:
        inc.append((A, f"la primera línea debe ser «{esperado}» (está «{primera[:80]}»)"))
    n = _tablas_sin_titulo(txt)
    if n:
        inc.append((A, f"la tabla de la línea {n[0]} no tiene título «Tabla N: …»"))
    if capturas_marcadas(txt):
        inc.append((A, "repite la marca «<!-- captura: … -->»: las capturas se marcan en 3.2 para que cada imagen entre una sola vez al informe"))
    desc = paginas_anexo(txt)
    for p in pags:
        if p["codigo"] not in desc:
            inc.append((A, f"{p['codigo']}: la página no tiene su «### {p['codigo']}. Nombre» con su descripción"))
        elif _vacio(desc[p["codigo"]]):
            inc.append((A, f"{p['codigo']}: falta la «**Descripción.**» de la página"))
    for c in sorted(set(desc) - {p["codigo"] for p in pags}):
        inc.append((A, f"{c}: describe una página que no está en 3.2"))
    return inc


def check_valores_json(valores, err, modelo):
    J = "valores.json"
    if err:
        return [(J, f"no es un JSON válido: {err}")]
    if valores is None:
        return [(J, "falta el archivo (el valor real de cada KPI lo entrega el equipo)")]
    inc = []
    if valores.get("schema") != 1:
        inc.append((J, "schema debe ser 1"))
    kpis = valores.get("kpis")
    if not isinstance(kpis, list) or not kpis:
        return inc + [(J, "kpis debe ser una lista con el valor real de cada KPI")]
    vistos = set()
    for x in kpis:
        c = x.get("codigo", "?")
        if c in vistos:
            inc.append((J, f"{c}: está repetido"))
        vistos.add(c)
        if _vacio(x.get("periodo")) or _vacio(x.get("unidad")):
            inc.append((J, f"{c}: faltan la unidad o el periodo"))
        if x.get("meta") is not None and not isinstance(x.get("meta"), (int, float)):
            inc.append((J, f"{c}: la meta debe ser un número o null"))
    if modelo is not None:
        for k in modelo.get("kpis", []):
            if k["codigo"] not in vistos:
                inc.append((J, f"{k['codigo']}: falta su valor real"))
        for c in sorted(vistos - {k["codigo"] for k in modelo.get("kpis", [])}):
            inc.append((J, f"{c}: no es un KPI de modelo.json"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_encabezados(run, PUNTOS) + D.check_marcador(run, PUNTOS) + D.check_citas(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    txt = D.texto(run, "3.2")
    modelo = None
    try:
        modelo, err = _json(D.corrida(raiz, D.MODELO) / "modelo.json")
        if modelo is None:
            inc.append(("secciones/3.2.md", "no se pueden comprobar las medidas ni los KPI sin el modelo.json de 07-make-data-model-kpi" + (f" ({err})" if err else "")))
    except D.SinCorrida as e:
        inc.append(("secciones/3.2.md", f"no se pueden comprobar las medidas ni los KPI sin la corrida de 07-make-data-model-kpi: {e}"))
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        br = None
        inc.append(("secciones/3.2.md", f"no se pueden comprobar los usuarios sin el brief vigente: {e}"))
    valores, verr = _json(run / "valores.json")
    pags = paginas(txt)
    inc += check_paginas(pags, modelo, br) + check_capturas(txt, pags, run)
    inc += check_valores_json(valores, verr, modelo)
    inc += check_valores(kpis_32(txt), pags, modelo, valores, run)
    inc += check_texto(txt, valores, modelo)
    return inc + check_anexo_c(run, modelo) + check_anexo_d(run, pags)
