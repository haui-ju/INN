"""Reglas del paso 10-make-storytelling (sección 4 y sus capturas; se invocan desde validate_run.py).

La sección 4 cuenta los resultados del dashboard como hallazgos HLZ-nn. Toda cifra sale de `valores.json` de la corrida vigente de
09-make-dashboard; el estado se calcula con el comparador de la meta de 2.5 (el mismo de rules/dashboard.py)."""
import filecmp
import re
from pathlib import Path

import brief as BR
import diagnostico as D
import projectcfg as P
import visuales as VI
from rules import dashboard as DB

PASO = "10-make-storytelling"
PUNTOS = ["4"]
UPDATE = "10-make-storytelling-update"
PREFIJOS = ("HLZ",)
S = "secciones/4.md"
COLUMNAS = ("Codigo", "Objetivo", "KPI", "Valor", "Meta", "Estado", "Captura", "Quien decide", "Decision")
RE_HLZ = re.compile(r"HLZ-\d+")
NUM = r"(\d{1,3}(?:[  ]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
RE_CIFRA = re.compile(rf"S/\s*{NUM}|{NUM}\s*(?:%|puntos porcentuales|puntos)")
RE_NEGOCIO_REAL = re.compile(r"negocio real", re.I)


def _vacio(t):
    return not (t or "").strip()


def _norm(t):
    return DB._norm(t)


def _num(t):
    return D.numero(t)


def _dec(t):
    """Decimales con que está escrita una cifra («97,2» -> 1)."""
    m = re.search(r"[.,](\d+)\s*$", re.sub(r"[^\d.,]", "", t or ""))
    return len(m.group(1)) if m else 0


# ------------------------------------------------------------------ lectura
def hallazgos(txt):
    """[{codigo, objetivo, kpi, valor, meta, estado, captura, quien, decision}] de la tabla de hallazgos."""
    t = VI.tabla(txt, *COLUMNAS)
    if not t:
        return []
    enc, filas = t
    return [{"codigo": f[0], "objetivo": VI._col(enc, f, "Objetivo"), "kpi": VI._col(enc, f, "KPI"), "valor": VI._col(enc, f, "Valor"),
             "meta": VI._col(enc, f, "Meta"), "estado": VI._col(enc, f, "Estado"), "captura": VI._col(enc, f, "Captura"),
             "quien": VI._col(enc, f, "Quien decide"), "decision": VI._col(enc, f, "Decision")} for f in filas if f and RE_HLZ.fullmatch(f[0])]


def bloques(txt):
    """{codigo: texto} de cada «### HLZ-nn. Título» hasta el siguiente encabezado."""
    lin = txt.splitlines()
    cab = [(i, m.group(1)) for i, l in enumerate(lin) if (m := re.match(r"^###\s+(HLZ-\d+)\b", l))]
    out = {}
    for n, (i, c) in enumerate(cab):
        fin = cab[n + 1][0] if n + 1 < len(cab) else len(lin)
        corte = next((j for j in range(i + 1, fin) if re.match(r"^\*\*(Prioridades|Metas pendientes)\.\*\*", lin[j])), fin)
        out[c] = "\n".join(lin[i:corte])
    return out


def cifras(texto):
    """[(texto, valor)] de las cifras con unidad (% o S/) de un texto."""
    out = []
    for m in RE_CIFRA.finditer(texto):
        t = m.group(1) or m.group(2)
        v = _num(t)
        if v is not None:
            out.append((m.group(0).strip(), t.strip(), v))
    return out


def sin_tablas_ni_contexto(txt):
    """El texto de la sección sin las filas de tabla ni el párrafo «Contexto» (que cita la problemática, no el dashboard)."""
    out, omitir = [], False
    for ln in txt.splitlines():
        if not ln.strip():
            omitir = False
            continue
        if ln.strip().startswith("**Contexto."):
            omitir = True
        if omitir or ln.strip().startswith("|"):
            continue
        out.append(ln)
    return "\n".join(out)


# ------------------------------------------------------------------ comprobaciones
def _permitidos(valores):
    """Valores que una cifra puede citar: el valor real, la meta y la diferencia entre ambos de cada KPI, y las medidas."""
    ok = []
    for k in (valores or {}).get("kpis", []):
        v, m = k.get("valor"), k.get("meta")
        if isinstance(v, (int, float)):
            ok.append(float(v))
            if isinstance(m, (int, float)):
                ok += [float(m), abs(float(v) - float(m))]
    for x in (valores or {}).get("medidas", []):
        if isinstance(x.get("valor"), (int, float)):
            ok.append(float(x["valor"]))
    return ok


def check_origen(raiz):
    """(corrida de 09, modelo, valores, brief, incidencias): lo que hay que leer para validar la sección."""
    inc, run9, modelo, valores, br = [], None, None, None, None
    try:
        run9 = D.corrida(raiz, "09-make-dashboard")
    except D.SinCorrida as e:
        inc.append((S, f"no se puede comprobar el dashboard sin la corrida de 09-make-dashboard: {e}"))
    if run9 is not None:
        valores, err = DB._json(run9 / "valores.json")
        if valores is None:
            inc.append((S, "la corrida vigente de 09-make-dashboard no trae valores.json: primero hay que entregar los valores del dashboard" + (f" ({err})" if err else "")))
    try:
        modelo, err = DB._json(D.corrida(raiz, D.MODELO) / "modelo.json")
        if modelo is None:
            inc.append((S, "no se pueden comprobar los KPI sin el modelo.json de 07-make-data-model-kpi" + (f" ({err})" if err else "")))
    except D.SinCorrida as e:
        inc.append((S, f"no se pueden comprobar los KPI sin la corrida de 07-make-data-model-kpi: {e}"))
    try:
        br = BR.vigente(raiz)
    except (BR.SinBrief, P.ConfigError) as e:
        inc.append((S, f"no se pueden comprobar los objetivos ni los usuarios sin el brief vigente: {e}"))
    return run9, modelo, valores, br, inc


def check_tabla(hall, modelo, br, valores, paginas, run):
    inc = []
    if not hall:
        return [(S, "falta la tabla de hallazgos «Código | Objetivo | KPI | Valor real | Meta | Estado | Captura | Quién decide | Decisión que apoya»")]
    kpis = {k["codigo"]: k for k in (modelo or {}).get("kpis", [])}
    vals = {x.get("codigo"): x for x in (valores or {}).get("kpis", [])}
    oes = {o["codigo"] for o in (br or {}).get("oe", [])}
    roles = DB._roles(br["usuarios"]) if br else None
    vistos = set()
    for h in hall:
        c = h["codigo"]
        if c in vistos:
            inc.append((S, f"{c}: el código de hallazgo está repetido"))
        vistos.add(c)
        if br is not None and h["objetivo"] not in oes:
            inc.append((S, f"{c}: «{h['objetivo']}» no es un objetivo específico del brief"))
        k = kpis.get(h["kpi"])
        if modelo is not None and k is None:
            inc.append((S, f"{c}: «{h['kpi']}» no es un KPI de modelo.json"))
            continue
        if k is not None and k.get("objetivo") != h["objetivo"]:
            inc.append((S, f"{c}: {h['kpi']} mide {k.get('objetivo')} y el hallazgo cita {h['objetivo']}"))
        v = vals.get(h["kpi"])
        if valores is not None and v is None:
            inc.append((S, f"{c}: el valor de {h['kpi']} no está en valores.json de 09-make-dashboard"))
            continue
        real = (v or {}).get("valor")
        if v is not None:
            citado = _num(h["valor"])
            if not isinstance(real, (int, float)) or isinstance(real, bool):
                inc.append((S, f"{c}: el valor de {h['kpi']} en valores.json no es un número"))
            elif citado is None or abs(citado - real) > 0.5 * 10 ** -_dec(h["valor"]) + 1e-9:
                inc.append((S, f"{c}: el valor «{h['valor']}» no coincide con valores.json ({real} para {h['kpi']})"))
        if h["estado"] not in DB.ESTADOS:
            inc.append((S, f"{c}: el estado debe ser uno de {', '.join(DB.ESTADOS)}"))
        elif k is not None:
            meta_md = k.get("meta", "")
            if _norm(h["meta"]) != _norm(meta_md):
                inc.append((S, f"{c}: la meta «{h['meta']}» no es la de modelo.json («{meta_md}»)"))
            if D.pendiente(meta_md):
                if h["estado"] != "Sin meta":
                    inc.append((S, f"{c}: {h['kpi']} no tiene meta, su estado debe ser «Sin meta» y el hallazgo no puede decir si cumple"))
            else:
                meta_n, cmp = _num(meta_md), DB._comparador(meta_md)
                if h["estado"] == "Sin meta":
                    inc.append((S, f"{c}: {h['kpi']} tiene meta «{meta_md}» y el estado es «Sin meta»"))
                elif cmp and meta_n is not None and isinstance(real, (int, float)):
                    cumple = real >= meta_n if cmp == ">=" else real <= meta_n
                    if cumple != (h["estado"] == "Cumple"):
                        inc.append((S, f"{c}: el estado «{h['estado']}» no concuerda con el valor {real} frente a la meta «{meta_md}»"))
        if _vacio(h["decision"]):
            inc.append((S, f"{c}: falta la decisión que apoya"))
        if _vacio(h["quien"]):
            inc.append((S, f"{c}: falta quién decide"))
        elif roles is not None and not any(r in _norm(h["quien"]) or _norm(h["quien"]) in r for r in roles):
            inc.append((S, f"{c}: «{h['quien']}» no es uno de los usuarios del brief ({br['usuarios']})"))
        cap = (h["captura"] or "").strip().lower()
        if _vacio(cap):
            inc.append((S, f"{c}: no cita ninguna captura del dashboard"))
            continue
        png = Path(run) / "capturas" / f"{cap}.png"
        if not png.is_file() or png.stat().st_size == 0:
            inc.append((S, f"{c}: cita la captura {cap}, que no está en capturas/ de esta corrida (cópiala desde la de 09-make-dashboard)"))
        esperada = paginas.get(h["kpi"])
        if esperada and cap != esperada:
            inc.append((S, f"{c}: {h['kpi']} se ve en {esperada.upper()} y el hallazgo cita {cap}"))
    for o in sorted(oes):
        if not any(h["objetivo"] == o for h in hall):
            inc.append((S, f"{o}: el objetivo no tiene ningún hallazgo"))
    return inc


def check_capturas(txt, hall, run9, run):
    inc = []
    marcadas = DB.capturas_marcadas(txt)
    citadas = []
    for h in hall:
        cap = (h["captura"] or "").strip().lower()
        if cap and cap not in citadas:
            citadas.append(cap)
    for cap in citadas:
        if marcadas.count(cap) != 1:
            inc.append((S, f"debe marcar una sola vez la captura con la línea «<!-- captura: {cap} -->» (está {marcadas.count(cap)} veces)"))
        if run9 is not None and (run9 / "capturas" / f"{cap}.png").is_file() and (Path(run) / "capturas" / f"{cap}.png").is_file():
            if not filecmp.cmp(run9 / "capturas" / f"{cap}.png", Path(run) / "capturas" / f"{cap}.png", shallow=False):
                inc.append((f"capturas/{cap}.png", "difiere de la captura de 09-make-dashboard: vuelve a copiarla"))
    for m in marcadas:
        if m not in citadas:
            inc.append((S, f"la captura «{m}» está marcada y ningún hallazgo la cita"))
    return inc


def check_texto(txt, hall, valores, modo_datos):
    inc = []
    parrafos = [p for p in re.split(r"\n\s*\n", txt.split("\n", 1)[1] if "\n" in txt else "") if p.strip()]
    if modo_datos == "generado":
        primero = next((p for p in parrafos if not p.lstrip().startswith(("**", "|", "<!--", "Tabla "))), "")
        if "generados para el proyecto" not in primero:
            inc.append((S, "con datos generados, el primer párrafo debe decir que los hallazgos se basan en «datos generados para el proyecto» y que no describen el negocio real de una empresa"))
    if _vacio(VI.campo(txt, "Contexto")):
        inc.append((S, "falta el «**Contexto.**» (la problemática y quién decide, sin cifras del dashboard)"))
    if _vacio(VI.campo(txt, "Prioridades")):
        inc.append((S, "falta las «**Prioridades.**» (qué decisión se toma primero y por qué)"))
    blq = bloques(txt)
    for h in hall:
        b = blq.get(h["codigo"])
        if b is None:
            inc.append((S, f"{h['codigo']}: falta su narrativa «### {h['codigo']}. Título»"))
            continue
        for rot in ("Qué muestra", "Qué decisión apoya"):
            if _vacio(VI.campo(b, rot)):
                inc.append((S, f"{h['codigo']}: falta el «**{rot}.**»"))
    for c in sorted(set(blq) - {h["codigo"] for h in hall}):
        inc.append((S, f"{c}: tiene narrativa y no está en la tabla de hallazgos"))
    if valores is not None:
        ok = _permitidos(valores)
        for crudo, t, v in cifras(sin_tablas_ni_contexto(txt)):
            tol = 0.5 * 10 ** -_dec(t) + 1e-9
            if not any(abs(v - a) <= tol for a in ok):
                inc.append((S, f"la cifra «{crudo}» no coincide con ningún valor, meta ni diferencia de valores.json"))
    for fr in re.split(r"(?<=[.!?])\s+", sin_tablas_ni_contexto(txt)):
        if RE_NEGOCIO_REAL.search(fr) and not re.search(r"\b(no|ni|sin)\b", fr, re.I):
            inc.append((S, f"no afirmes que los hallazgos describen el negocio real: «{fr.strip()[:70]}»"))
            break
    comentarios = [ln for ln in txt.splitlines() if "<!--" in ln and not DB.RE_CAPTURA.match(ln.strip())]
    if comentarios:
        inc.append((S, f"comentario que no es una marca de captura: «{comentarios[0].strip()[:60]}» (el texto es final, sin notas)"))
    n = DB._tablas_sin_titulo(txt)
    if n:
        inc.append((S, f"la tabla de la línea {n[0]} no tiene título «Tabla N: …»"))
    return inc


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inc = D.check_encabezados(run, PUNTOS) + D.check_marcador(run, PUNTOS) + D.check_citas(run, PUNTOS)
    if D.faltan_secciones(inc):
        return inc
    txt = D.texto(run, "4")
    run9, modelo, valores, br, falta = check_origen(raiz)
    inc += falta
    paginas = {}
    if run9 is not None:
        t32 = D.texto(run9, "3.2")
        if t32:
            paginas = {k["codigo"]: k["pagina"].strip().lower() for k in DB.kpis_32(t32)}
    try:
        modo = P.load(raiz).get("modo_datos")
    except P.ConfigError:
        modo = None
    hall = hallazgos(txt)
    inc += check_tabla(hall, modelo, br, valores, paginas, run)
    inc += check_capturas(txt, hall, run9, run)
    inc += check_texto(txt, hall, valores, modo)
    return inc
