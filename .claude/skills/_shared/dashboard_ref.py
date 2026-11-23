#!/usr/bin/env python3
"""Dashboard de referencia (paso 09-make-dashboard): HTML con el diseño del proyecto y guía paso a paso para construirlo en Power BI.

  python3 .claude/skills/_shared/dashboard_ref.py plan      --run CORRIDA [--raiz .]   (copia el plan por defecto a materiales/paginas.json)
  python3 .claude/skills/_shared/dashboard_ref.py construir --run CORRIDA [--raiz .]   (escribe dashboard-referencia.html, guia-dashboard.md y los .txt)

Lee `materiales/paginas.json` de la corrida (páginas, visuales, medidas y columnas calculadas), los valores esperados de `data/respuestas/`
(ya calculados por el generador: aquí no se recalcula nada desde los archivos brutos), `modelo.json` y las metas de 07, los usuarios del brief y los
tokens del sistema de diseño. El HTML es autónomo (sin recursos externos) y trae el tema claro y el oscuro. Solo biblioteca estándar.
La referencia muestra lo que el equipo debería obtener; no es el dashboard: este se construye en Power BI.
"""
import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dashboard_dax as DAX  # noqa: E402
import diagnostico as D  # noqa: E402
import html_tpl as H  # noqa: E402

PLAN_POR_DEFECTO = HERE.parents[2] / "common" / "09-dashboard" / "paginas-por-defecto.json"
CANALES = ["Salón", "Para llevar", "WhatsApp", "Rappi", "PedidosYa"]
COLOR_CANAL = {"Salón": 1, "Para llevar": 3, "WhatsApp": 6, "Rappi": 4, "PedidosYa": 2}
TURNOS = ["Mañana", "Tarde", "Noche"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MES_ABR = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
TIPOS = ("tarjeta", "linea", "columnas", "apiladas", "apiladas100", "barras", "matriz", "tabla")
FUENTES = ("kpi_mensual", "ventas_canal_mes", "comision_mes", "margen_canal", "margen_canal_producto", "merma_turno", "merma_dia",
           "prep_vend_dia", "vendidos_pronostico", "precio_dia", "precio_mes", "tabla_kpi")
ANCHO, ALTO, PAD, HUECO, ENCABEZADO, TARJETAS = 1600, 900, 24, 16, 76, 120
ESPACIO = "\u00a0"


class ErrorReferencia(Exception):
    """Falta un insumo (plan, respuestas, modelo) o el plan no es coherente."""


# ------------------------------------------------------------------ entradas
def _csv(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cargar_respuestas(raiz):
    d = Path(raiz) / "data" / "respuestas"
    if not d.is_dir():
        raise ErrorReferencia(f"faltan los valores esperados en {d}: genera los datos con 08-make-etl")
    return {f.stem: _csv(f) for f in sorted(d.glob("*.csv"))}


def cargar_plan(run):
    f = Path(run) / "materiales" / "paginas.json"
    if not f.is_file():
        raise ErrorReferencia(f"falta {f}: usa `dashboard_ref.py plan --run <corrida>` o escribe el plan confirmado")
    return json.loads(f.read_text(encoding="utf-8"))


def cargar_modelo(raiz):
    try:
        return json.loads((D.corrida(raiz, D.MODELO) / "modelo.json").read_text(encoding="utf-8"))
    except (D.SinCorrida, OSError, ValueError) as e:
        raise ErrorReferencia(f"falta el modelo.json de 07-make-data-model-kpi: {e}")


def parse_meta(texto):
    """(comparador, valor) de una meta como «12 % o más»; (None, None) si es «Pendiente» o no tiene número."""
    m = re.search(r"(\d+(?:[.,]\d+)?)", texto or "")
    t = DAX.norm(texto)
    if not m or "pendiente" in t:
        return None, None
    v = float(m.group(1).replace(",", "."))
    return ("<=" if re.search(r"o menos|como maximo", t) else ">=" if re.search(r"o mas|como minimo", t) else ">="), v


def estado(valor, comparador, meta):
    if comparador is None or valor is None:
        return "Sin meta"
    return "Cumple" if (valor >= meta if comparador == ">=" else valor <= meta) else "No cumple"


def metas_kpi(modelo):
    return {k["codigo"]: {**{"nombre": k["nombre"], "meta_texto": k["meta"], "frecuencia": k.get("frecuencia", "")}, "cmp": parse_meta(k["meta"])[0],
                          "meta": parse_meta(k["meta"])[1]} for k in modelo.get("kpis", [])}


# ------------------------------------------------------------------ valores esperados por fuente
def etiqueta_mes(m):
    return f"{MES_ABR[int(m[5:7]) - 1]} {m[2:4]}"


def _num(x):
    return float(x) if x not in ("", None) else None


def kpi_serie(resp, kpi):
    f = [r for r in resp["kpi-esperados"] if r["kpi"] == kpi and r["valor"] != ""]
    return [r["mes"] for r in f], [float(r["valor"]) for r in f]


def datos_visual(v, resp, modelo, metas):
    """{'cats', 'series': [{'nombre','valores','color'}], ...} con los valores esperados de la hoja de respuestas para ese visual."""
    d = v["datos"]
    f = d["fuente"]
    if f == "kpi_mensual":
        meses, vals = kpi_serie(resp, d["kpi"])
        return {"cats": [etiqueta_mes(m) for m in meses], "series": [{"nombre": metas[d["kpi"]]["nombre"], "valores": vals, "color": 1}]}
    if f in ("ventas_canal_mes", "comision_mes"):
        meses = sorted({r["mes"] for r in resp["ventas-mes-canal"]})
        por = {(r["mes"], r["canal"]): r for r in resp["ventas-mes-canal"]}
        if f == "comision_mes":
            vals = [sum(float(por[(m, c)]["comision"]) for c in CANALES if (m, c) in por) for m in meses]
            return {"cats": [etiqueta_mes(m) for m in meses], "series": [{"nombre": "Comisión pagada", "valores": vals, "color": 4}]}
        series = [{"nombre": c, "valores": [float(por[(m, c)]["ventas"]) if (m, c) in por else 0.0 for m in meses], "color": COLOR_CANAL[c]} for c in CANALES]
        if d.get("modo") == "participacion":
            tot = [sum(s["valores"][i] for s in series) for i in range(len(meses))]
            for s in series:
                s["valores"] = [100 * x / t if t else 0.0 for x, t in zip(s["valores"], tot)]
        return {"cats": [etiqueta_mes(m) for m in meses], "series": series}
    if f == "margen_canal":
        acum = {}
        for r in resp["margen-canal-producto"]:
            a = acum.setdefault(r["canal"], [0.0, 0.0, 0.0])
            a[0] += float(r["ventas"]); a[1] += float(r["comision"]); a[2] += float(r["costo_estimado"])
        filas = sorted(((c, 100 * (a[0] - a[1] - a[2]) / a[0]) for c, a in acum.items()), key=lambda x: -x[1])
        return {"cats": [c for c, _ in filas], "series": [{"nombre": "Margen de contribución", "valores": [x for _, x in filas], "color": 1}]}
    if f == "margen_canal_producto":
        acum = {}
        for r in resp["margen-canal-producto"]:
            a = acum.setdefault((r["producto"], r["canal"]), [0.0, 0.0, 0.0])
            a[0] += float(r["ventas"]); a[1] += float(r["comision"]); a[2] += float(r["costo_estimado"])
        productos = list(dict.fromkeys(r["producto"] for r in resp["margen-canal-producto"]))
        return {"filas": productos, "columnas": CANALES,
                "valores": {(p, c): 100 * (a[0] - a[1] - a[2]) / a[0] for (p, c), a in acum.items()}}
    if f == "merma_turno":
        acum = {}
        for r in resp["produccion-mes-turno"]:
            a = acum.setdefault(r["turno"], [0, 0])
            a[0] += int(r["merma"]); a[1] += int(r["preparados"])
        return {"cats": TURNOS, "series": [{"nombre": "Merma", "valores": [100 * acum[t][0] / acum[t][1] for t in TURNOS], "color": 4}]}
    if f in ("merma_dia", "prep_vend_dia"):
        dias = {r["dia_semana"]: r for r in resp["produccion-dia-semana"]}
        if f == "merma_dia":
            return {"cats": DIAS, "series": [{"nombre": "Merma", "valores": [float(dias[x]["merma_pct"]) for x in DIAS], "color": 4}]}
        return {"cats": DIAS, "series": [{"nombre": "Pollos preparados", "valores": [float(dias[x]["preparados"]) for x in DIAS], "color": 3},
                                         {"nombre": "Pollos vendidos", "valores": [float(dias[x]["vendidos"]) for x in DIAS], "color": 1}]}
    if f == "vendidos_pronostico":
        por = {}
        for r in resp["pronostico-referencia"]:
            a = por.setdefault(r["fecha"], [0.0, 0.0])
            a[0] += float(r["vendidos"]); a[1] += float(r["pronostico"])
        dias = sorted(por)[-28:]
        return {"cats": [f"{x[8:10]}/{x[5:7]}" for x in dias],
                "series": [{"nombre": "Pollos vendidos", "valores": [por[x][0] for x in dias], "color": 1},
                           {"nombre": "Pronóstico de referencia", "valores": [por[x][1] for x in dias], "color": 3, "punteada": True}]}
    if f == "precio_dia":
        filas = resp["precio-dia"]
        return {"cats": [r["fecha"] for r in filas], "series": [{"nombre": "Precio por kg", "valores": [float(r["precio_kg"]) for r in filas], "color": 1}],
                "marcas": [i for i, r in enumerate(filas) if r["imputado"] == "1"], "diario": True}
    if f == "precio_mes":
        meses, vals = kpi_serie(resp, "KPI-06")
        return {"cats": [etiqueta_mes(m) for m in meses], "series": [{"nombre": "Precio promedio", "valores": vals, "color": 1}]}
    if f == "tabla_kpi":
        filas = []
        ultimo = max(r["mes"] for r in resp["kpi-esperados"])
        for k, m in metas.items():
            r = next((x for x in resp["kpi-esperados"] if x["kpi"] == k and x["mes"] == ultimo and x["valor"] != ""), None)
            if k == "KPI-07":
                con = sum(1 for x in metas.values() if x["meta"] is not None)
                valor = 100 * con / len(metas)
            else:
                valor = float(r["valor"]) if r else None
            filas.append({"kpi": k, "nombre": m["nombre"], "valor": valor, "unidad": "S/ por kg" if k == "KPI-06" else "%", "meta_texto": m["meta_texto"],
                          "estado": estado(valor, m["cmp"], m["meta"])})
        return {"filas": filas, "mes": ultimo}
    raise ErrorReferencia(f"fuente de datos desconocida: {f}")


def valor_kpi(resp, kpi, metas):
    """Valor esperado del último mes y su estado para una tarjeta."""
    if kpi == "KPI-07":
        con = sum(1 for x in metas.values() if x["meta"] is not None)
        valor, mes = 100 * con / len(metas), max(r["mes"] for r in resp["kpi-esperados"])
    else:
        meses, vals = kpi_serie(resp, kpi)
        valor, mes = (vals[-1], meses[-1]) if vals else (None, "")
    m = metas[kpi]
    return {"kpi": kpi, "nombre": m["nombre"], "valor": valor, "mes": mes, "meta_texto": m["meta_texto"], "estado": estado(valor, m["cmp"], m["meta"]),
            "unidad": "S/ por kg" if kpi == "KPI-06" else "%"}


# ------------------------------------------------------------------ formato
def fmt(v, unidad, corto=False):
    if v is None:
        return "—"
    if unidad == "%":
        return f"{v:.1f} %"
    if unidad == "S/":
        return f"S/{ESPACIO}{v / 1000:.0f}{ESPACIO}mil" if corto and abs(v) >= 10000 else f"S/{ESPACIO}{round(v):,}".replace(",", ESPACIO)
    if unidad == "S/ por kg":
        return f"S/{ESPACIO}{v:.2f}"
    return f"{round(v):,}".replace(",", ESPACIO)


def esc(t):
    return html.escape(str(t), quote=True)


def escala(vmin, vmax, n=4):
    """(mínimo, máximo, marcas) con valores redondos."""
    if vmax <= vmin:
        vmax = vmin + 1
    paso = (vmax - vmin) / n
    base = 10 ** (len(str(int(paso))) - 1 if paso >= 1 else -1)
    for m in (1, 2, 2.5, 5, 10):
        if m * base >= paso:
            paso = m * base
            break
    lo = (vmin // paso) * paso
    hi = lo
    marcas = [lo]
    while hi < vmax - 1e-9:
        hi += paso
        marcas.append(round(hi, 10))
    return lo, hi, marcas


# ------------------------------------------------------------------ gráficos (SVG)
def _t(x, y, texto, ancla="start", tam=14, clase="eje", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" font-size="{tam}" class="{clase}" {extra}>{esc(texto)}</text>'


def _marcas_x(cats, paso_max=8):
    n = len(cats)
    paso = max(1, -(-n // paso_max))
    return [i for i in range(0, n, paso)]


def _rect_redondo(x, y, w, h, r=4, arriba=True):
    """Rectángulo con las esquinas de arriba redondeadas (el extremo del dato) y la base recta."""
    r = min(r, w / 2, h)
    if h <= 0:
        return ""
    return (f"M{x:.1f},{y + h:.1f} L{x:.1f},{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} L{x + w - r:.1f},{y:.1f} "
            f"Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} L{x + w:.1f},{y + h:.1f} Z")


def _ejes(W, H, lo, hi, marcas, unidad, izq):
    der, sup, inf = 12, 10, 30
    h = H - sup - inf
    g = []
    for m in marcas:
        y = sup + h * (1 - (m - lo) / (hi - lo))
        g.append(f'<line x1="{izq}" x2="{W - der}" y1="{y:.1f}" y2="{y:.1f}" class="rejilla"/>')
        etiqueta = f"{int(m)} %" if unidad == "%" and float(m).is_integer() else fmt(m, unidad, True)
        g.append(_t(izq - 8, y + 5, etiqueta, "end"))
    return g, (izq, W - der, sup, H - inf)


def svg_linea(W, H, datos, unidad, meta=None, titulo=""):
    cats, series = datos["cats"], datos["series"]
    todos = [x for s in series for x in s["valores"]] + ([meta[1]] if meta else [])
    lo, hi, marcas = escala(min(0, min(todos)) if unidad in ("S/", "pollos") else max(0, min(todos) * 0.85), max(todos) * 1.05)
    izq = 88 if unidad == "S/" else 64
    g, (x0, x1, y0, y1) = _ejes(W, H, lo, hi, marcas, unidad, izq)
    n = len(cats)
    xs = [x0 + (x1 - x0 - 20) * (i / max(1, n - 1)) + 10 for i in range(n)]
    yv = lambda v: y0 + (y1 - y0) * (1 - (v - lo) / (hi - lo))
    for i in _marcas_x(cats, 8 if not datos.get("diario") else 7):
        g.append(_t(xs[i], H - 8, cats[i] if not datos.get("diario") else f"{etiqueta_mes(cats[i][:7])}", "middle"))
    if meta:
        g.append(f'<line x1="{x0}" x2="{x1}" y1="{yv(meta[1]):.1f}" y2="{yv(meta[1]):.1f}" class="meta"/>')
        g.append(_t(x1, yv(meta[1]) - 6, meta[0], "end", 14, "etq-meta"))
    for s in series:
        pts = " ".join(f"{xs[i]:.1f},{yv(v):.1f}" for i, v in enumerate(s["valores"]))
        dash = ' stroke-dasharray="7 5"' if s.get("punteada") else ""
        g.append(f'<polyline points="{pts}" fill="none" stroke="var(--c-serie-{s["color"]})" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
        ult = len(s["valores"]) - 1
        g.append(f'<circle cx="{xs[ult]:.1f}" cy="{yv(s["valores"][ult]):.1f}" r="5" fill="var(--c-serie-{s["color"]})" stroke="var(--c-superficie)" stroke-width="2"/>')
        if len(series) == 1 and not datos.get("diario"):
            g.append(_t(xs[ult] - 10, yv(s["valores"][ult]) - 16, fmt(s["valores"][ult], unidad), "end", 14, "valor"))
    for i in datos.get("marcas", []):
        v = series[0]["valores"][i]
        g.append(f'<circle cx="{xs[i]:.1f}" cy="{yv(v):.1f}" r="4" fill="var(--c-superficie)" stroke="var(--c-serie-4)" stroke-width="2.5"><title>Día sin precio: se usó el último publicado</title></circle>')
    g.append(f'<line class="cruz" x1="-10" x2="-10" y1="{y0}" y2="{y1}"/>')
    ancho_hit = (x1 - x0) / max(1, n)
    for i in range(n):
        tip = f"<b>{esc(cats[i])}</b>" + "".join(f"<br>{esc(s['nombre'])}: {fmt(s['valores'][i], unidad)}" for s in series)
        g.append(f'<rect x="{xs[i] - ancho_hit / 2:.1f}" y="{y0}" width="{ancho_hit:.1f}" height="{y1 - y0}" fill="transparent" data-x="{xs[i]:.1f}" data-tip="{esc(tip)}"/>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}">{"".join(g)}</svg>'


def svg_columnas(W, H, datos, unidad, modo="agrupadas", meta=None, titulo=""):
    cats, series = datos["cats"], datos["series"]
    n, k = len(cats), len(series)
    if modo == "apiladas100":
        lo, hi, marcas = 0, 100, [0, 25, 50, 75, 100]
    elif modo == "apiladas":
        tope = max(sum(s["valores"][i] for s in series) for i in range(n))
        lo, hi, marcas = escala(0, tope * 1.05)
    else:
        tope = max(x for s in series for x in s["valores"] + ([meta[1]] if meta else []))
        lo, hi, marcas = escala(0, tope * 1.1)
    izq = 88 if unidad == "S/" else 64
    g, (x0, x1, y0, y1) = _ejes(W, H, lo, hi, marcas, unidad if modo != "apiladas100" else "%", izq)
    yv = lambda v: y0 + (y1 - y0) * (1 - (v - lo) / (hi - lo))
    banda = (x1 - x0) / n
    ancho = min(banda * 0.62, 56) if modo != "agrupadas" or k == 1 else min(banda * 0.7 / k, 30)
    for i in range(n):
        cx = x0 + banda * (i + 0.5)
        if modo in ("apiladas", "apiladas100"):
            base = 0.0
            for s in series:
                v = s["valores"][i]
                if v <= 0:
                    continue
                ytop, ybase = yv(base + v), yv(base)
                tip = f"<b>{esc(cats[i])}</b><br>{esc(s['nombre'])}: {fmt(v, unidad)}"
                g.append(f'<rect x="{cx - ancho / 2:.1f}" y="{ytop:.1f}" width="{ancho:.1f}" height="{max(0, ybase - ytop):.1f}" fill="var(--c-serie-{s["color"]})" '
                         f'stroke="var(--c-superficie)" stroke-width="2" data-tip="{esc(tip)}"/>')
                base += v
        else:
            total = ancho * k + 4 * (k - 1)
            for j, s in enumerate(series):
                v = s["valores"][i]
                x = cx - total / 2 + j * (ancho + 4)
                tip = f"<b>{esc(cats[i])}</b><br>{esc(s['nombre'])}: {fmt(v, unidad)}"
                g.append(f'<path d="{_rect_redondo(x, yv(v), ancho, yv(0) - yv(v))}" fill="var(--c-serie-{s["color"]})" data-tip="{esc(tip)}"/>')
                if k == 1 and n <= 8:
                    g.append(_t(cx, yv(v) - 7, fmt(v, unidad), "middle", 14, "valor"))
        if i in _marcas_x(cats, 12):
            g.append(_t(cx, H - 8, cats[i][:3] if len(cats[i]) > 8 and cats[i] in DIAS else cats[i], "middle"))
    if meta:
        g.append(f'<line x1="{x0}" x2="{x1}" y1="{yv(meta[1]):.1f}" y2="{yv(meta[1]):.1f}" class="meta"/>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}">{"".join(g)}</svg>'


def svg_barras(W, H, datos, unidad, titulo=""):
    cats, vals = datos["cats"], datos["series"][0]["valores"]
    n = len(cats)
    izq, der, sup = 110, 64, 6
    banda = (H - sup - 8) / n
    tope = max(vals)
    g = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = sup + banda * i + banda * 0.18
        h = banda * 0.64
        w = (W - izq - der) * v / tope
        tip = f"<b>{esc(c)}</b><br>{fmt(v, unidad)}"
        g.append(_t(izq - 10, y + h / 2 + 5, c, "end", 16, "cat"))
        g.append(f'<path d="M{izq},{y:.1f} L{izq + w - 4:.1f},{y:.1f} Q{izq + w:.1f},{y:.1f} {izq + w:.1f},{y + 4:.1f} L{izq + w:.1f},{y + h - 4:.1f} '
                 f'Q{izq + w:.1f},{y + h:.1f} {izq + w - 4:.1f},{y + h:.1f} L{izq},{y + h:.1f} Z" fill="var(--c-serie-1)" data-tip="{esc(tip)}"/>')
        g.append(_t(izq + w + 8, y + h / 2 + 5, fmt(v, unidad), "start", 16, "valor"))
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}">{"".join(g)}</svg>'


def html_matriz(datos, unidad):
    vals = datos["valores"]
    lo, hi = min(vals.values()), max(vals.values())
    cab = "".join(f"<th>{esc(c)}</th>" for c in datos["columnas"])
    filas = []
    for p in datos["filas"]:
        celdas = []
        for c in datos["columnas"]:
            v = vals.get((p, c))
            if v is None:
                celdas.append("<td>—</td>")
                continue
            peso = 8 + 62 * (v - lo) / (hi - lo if hi > lo else 1)
            celdas.append(f'<td style="background:color-mix(in srgb, var(--c-serie-3) {peso:.0f}%, var(--c-superficie))" data-tip="{esc(p)} · {esc(c)}<br>{fmt(v, unidad)}">{fmt(v, unidad)}</td>')
        filas.append(f"<tr><th>{esc(p)}</th>{''.join(celdas)}</tr>")
    return f'<table class="matriz"><thead><tr><th></th>{cab}</tr></thead><tbody>{"".join(filas)}</tbody></table>'


ICONO = {"Cumple": "✔", "No cumple": "✖", "Sin meta": "–"}
CLASE = {"Cumple": "ok", "No cumple": "mal", "Sin meta": "sin"}


def html_tabla_kpi(datos):
    filas = "".join(f'<tr><td class="cod">{esc(f["kpi"])}</td><td>{esc(f["nombre"])}</td><td class="der">{fmt(f["valor"], f["unidad"])}</td><td>{esc(f["meta_texto"])}</td>'
                    f'<td><span class="chip {CLASE[f["estado"]]}"><span aria-hidden="true">{ICONO[f["estado"]]}</span> {esc(f["estado"])}</span></td></tr>' for f in datos["filas"])
    return (f'<table class="tkpi"><thead><tr><th>Código</th><th>KPI</th><th class="der">Valor ({esc(etiqueta_mes(datos["mes"]))})</th><th>Meta</th><th>Estado</th></tr></thead>'
            f"<tbody>{filas}</tbody></table>")


def html_tarjeta(k):
    return (f'<div class="tarjeta"><div class="t-etq"><span class="cod">{esc(k["kpi"])}</span> {esc(k["nombre"])}</div>'
            f'<div class="t-fila"><span class="t-valor">{fmt(k["valor"], k["unidad"])}</span>'
            f'<span class="chip {CLASE[k["estado"]]}"><span aria-hidden="true">{ICONO[k["estado"]]}</span> {esc(k["estado"])}</span></div>'
            f'<div class="t-meta">Meta: {esc(k["meta_texto"])} · {esc(etiqueta_mes(k["mes"]))}</div></div>')


def leyenda(series, meta=None, marcas=False):
    """Leyenda con una entrada por serie (si hay dos o más), más la meta y los días sin precio cuando el gráfico los dibuja."""
    items = []
    if len(series) >= 2:
        items += [f'<span><i style="background:var(--c-serie-{s["color"]})"></i>{esc(s["nombre"])}</span>' for s in series]
    if meta:
        items.append(f'<span><i class="k-meta"></i>{esc(meta[0])}</span>')
    if marcas:
        items.append('<span><i class="k-marca"></i>Día sin precio</span>')
    return '<div class="leyenda">' + "".join(items) + "</div>" if items else ""


def meta_de(v, metas):
    m = v.get("meta")
    if not m:
        return None
    if "kpi" in m:
        k = metas[m["kpi"]]
        return (f"Meta {k['meta']:g} %", k["meta"]) if k["meta"] is not None else None
    return (m.get("etiqueta", ""), m["valor"])


# ------------------------------------------------------------------ geometría del lienzo
def geometria(pagina):
    tiene = bool(pagina.get("kpis"))
    area = ALTO - 2 * PAD - ENCABEZADO - HUECO - ((TARJETAS + HUECO) if tiene else 0)
    filas = max(v["pos"][1] + v["pos"][3] - 1 for v in pagina["visuales"])
    alto_fila = (area - HUECO * (filas - 1)) / filas
    ancho_col = (ANCHO - 2 * PAD - 11 * HUECO) / 12
    return area, alto_fila, ancho_col


def tam_visual(v, pagina):
    _, alto_fila, ancho_col = geometria(pagina)
    c, f, w, h = v["pos"]
    ancho = ancho_col * w + HUECO * (w - 1)
    alto = alto_fila * h + HUECO * (h - 1)
    return ancho, alto


def render_visual(v, pagina, resp, modelo, metas):
    ancho, alto = tam_visual(v, pagina)
    unidad = v.get("unidad", "")
    datos = datos_visual(v, resp, modelo, metas)
    W, H = int(ancho - 28), int(alto - 14 - 38 - 12)
    meta = meta_de(v, metas)
    t = v["tipo"]
    if t == "linea":
        cuerpo = svg_linea(W, H, datos, unidad, meta, v["titulo"])
    elif t == "columnas":
        cuerpo = svg_columnas(W, H, datos, unidad, "agrupadas", meta, v["titulo"])
    elif t == "apiladas":
        cuerpo = svg_columnas(W, H, datos, unidad, "apiladas", None, v["titulo"])
    elif t == "apiladas100":
        cuerpo = svg_columnas(W, H, datos, "%", "apiladas100", None, v["titulo"])
    elif t == "barras":
        cuerpo = svg_barras(W, H, datos, unidad, v["titulo"])
    elif t == "matriz":
        cuerpo = html_matriz(datos, unidad)
    elif t == "tabla":
        cuerpo = html_tabla_kpi(datos)
    else:
        raise ErrorReferencia(f"tipo de visual desconocido: {t}")
    c, f, w, h = v["pos"]
    leyenda_html = leyenda(datos["series"], meta if t == "columnas" else None, bool(datos.get("marcas"))) if "series" in datos else ""
    return (f'<figure class="visual" data-caja="{pagina["codigo"]}-{v["id"]}" tabindex="0" role="button" title="Clic para ver cómo construirlo" style="grid-column:{c} / span {w};grid-row:{f} / span {h}">'
            f'<figcaption><span class="num">{v["id"]}</span><span class="v-titulo">{esc(v["titulo"])}</span>{leyenda_html}</figcaption>'
            f'<div class="cuerpo">{cuerpo}</div></figure>')


# ------------------------------------------------------------------ "Cómo construirlo"
NOMBRE_TIPO = {"tarjeta": "Tarjeta", "linea": "Gráfico de líneas", "columnas": "Gráfico de columnas agrupadas", "apiladas": "Gráfico de columnas apiladas",
               "apiladas100": "Gráfico de columnas apiladas al 100 %", "barras": "Gráfico de barras agrupadas (horizontales)", "matriz": "Matriz", "tabla": "Tabla"}


def nombres_medidas(plan, codigos):
    por = {m["codigo"]: m for m in plan["medidas"]}
    return [f"[{por[c]['nombre']}]" for c in codigos if c in por]


def esperado_resumen(v, resp, modelo, metas):
    d = datos_visual(v, resp, modelo, metas)
    u = v.get("unidad", "")
    if "series" in d and d["series"]:
        s = d["series"][0]
        n = len(s["valores"])
        if d.get("diario"):
            return f"{d['cats'][0]}: {fmt(s['valores'][0], u)}; 14/07/2026: {fmt(s['valores'][d['cats'].index('2026-07-14')], u)}; {d['cats'][-1]}: {fmt(s['valores'][-1], u)}"
        if len(d["series"]) > 1 and v["tipo"] in ("apiladas", "apiladas100"):
            return "; ".join(f"{x['nombre']}: {fmt(x['valores'][0], u)} → {fmt(x['valores'][-1], u)}" for x in d["series"] if x["valores"])
        if len(d["series"]) > 1:
            return f"{d['cats'][-1]}: " + "; ".join(f"{x['nombre']} {fmt(x['valores'][-1], u)}" for x in d["series"])
        if v["tipo"] in ("columnas", "barras"):
            return "; ".join(f"{c}: {fmt(x, u)}" for c, x in zip(d["cats"], s["valores"]))
        return f"{d['cats'][0]}: {fmt(s['valores'][0], u)} → {d['cats'][-1]}: {fmt(s['valores'][-1], u)}"
    if "valores" in d:
        vals = d["valores"]
        return f"de {fmt(min(vals.values()), u)} a {fmt(max(vals.values()), u)}"
    return f"{len(d['filas'])} filas, mes {etiqueta_mes(d['mes'])}"


RE_REF = re.compile(r"\b([fd][A-Z]\w*)\[(\w+)\]")
ORDEN_POR = {"nombre_mes": "mes", "dia_semana": "num_dia_semana", "mes_anio": "anio_mes", "turno": "turno_key", "canal": "canal_key", "producto": "producto_key", "kpi": "kpi_key"}


def _ref_html(tabla, col):
    return f"<b>{esc(col)}</b> de la tabla <b>{esc(tabla)}</b>"


def _csv_de(tabla):
    return f"data/limpio/{tabla}.csv"


def campo_eje_html(texto):
    """'dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])' → de qué tabla y columna sale y cómo se ordena."""
    m = RE_REF.search(texto)
    if not m:
        return esc(texto)
    tabla, col = m.groups()
    out = f"Columna {_ref_html(tabla, col)} (archivo <code>{esc(_csv_de(tabla))}</code>)."
    o = re.search(r"ordenada por \w+\[(\w+)\]", texto)
    if o:
        out += f" Ordénala por <b>{esc(o.group(1))}</b>: selecciona la columna en el panel Datos ▸ Herramientas de columna ▸ Ordenar por columna."
    elif "lunes a domingo" in texto:
        out += f" Ordénala de lunes a domingo: Ordenar por columna ▸ <b>{ORDEN_POR.get(col, 'num_dia_semana')}</b>."
    return out


MEDIDAS_CREADAS = set()  # nombres de medidas que el equipo ya creó: se muestran sin su DAX


def medidas_html(plan, v, codigos):
    g = _Guia(plan, {}, {}, {})
    out = []
    for c in codigos:
        m = g.por_codigo.get(c)
        if not m:
            continue
        if m["nombre"] in MEDIDAS_CREADAS:
            out.append(f'<div class="med"><b>[{esc(m["nombre"])}]</b> · ✔ ya la creaste (no hay que hacer nada)</div>')
            continue
        cols = g.columnas(g.recursivas([c]))
        orig = ", ".join(f"{t}[{k}]" for t, k in cols)
        previas = [n for n in dict.fromkeys(RE_MEDIDA.findall(m["dax"])) if n in g.por_nombre and n != m["nombre"]]
        previas_txt = f" Usa antes las medidas: {', '.join('[' + n + ']' for n in previas)} (créalas primero)." if previas else ""
        out.append(f'<div class="med"><b>[{esc(m["nombre"])}]</b> · medida DAX, créala en la tabla <b>Medidas</b> (Nueva medida)<code>{esc(m["dax"])}</code>'
                   f'<span>Sale de las columnas: {esc(orig) if orig else "otras medidas"}.{esc(previas_txt)}</span></div>')
    return "".join(out)


HEX_SERIE = {1: ("verde azulado", "#009385"), 2: ("rojo", "#BF5354"), 3: ("azul", "#3A7BCB"), 4: ("ámbar", "#B36300"), 5: ("morado", "#8864C0"),
             6: ("verde", "#319047"), 7: ("rosa", "#B55386")}


def formato_medida(unidad):
    """Cómo dar formato a la medida (si no, el eje sale como 0.0 a 0.7 en vez de 0 % a 70 %)."""
    if unidad == "%":
        return "Porcentaje, 1 decimal"
    if unidad == "S/":
        return "Moneda con símbolo S/, 0 decimales"
    if unidad == "S/ por kg":
        return "Moneda con símbolo S/, 2 decimales"
    return "Número entero con separador de miles"


def pasos_diseno(v, datos, unidad):
    t = v["tipo"]
    colores = []
    for sr in datos.get("series", []):
        nom, hx = HEX_SERIE.get(sr["color"], ("", ""))
        colores.append(f"{sr['nombre']}: {hx} ({nom})")
    p = ["Selecciona el visual y en Visualizaciones abre la pestaña <b>Formato</b> (icono del pincel) ▸ <b>Elementos visuales</b>."]
    if t == "barras":
        p += ["<b>Barras ▸ Colores ▸ Color predeterminado</b>: " + esc(colores[0] if colores else "#009385") + ". Si queda azul, es el color por defecto de Power BI y no lo cambiaste.",
              "<b>Barras ▸ Diseño</b>: baja el espacio entre categorías (o sube el ancho de barra) hasta que las barras queden gruesas.",
              "<b>Eje X (valores)</b>: apaga el interruptor (la referencia no lo muestra) y apaga la <b>Cuadrícula</b>. Así desaparece la escala 0.0 a 0.7.",
              "<b>Eje Y (categorías)</b>: apaga el <b>Título</b> del eje y deja el texto en 14 pt.",
              f"<b>General ▸ Título ▸ Texto</b>: escribe «{esc(v['titulo'])}» tú mismo (el automático sale como «medida por canal»). Apaga el <b>Subtítulo</b>."]
    elif t in ("columnas", "apiladas", "apiladas100"):
        p += ["<b>Columnas ▸ Colores</b>: " + esc("; ".join(colores)) + ". En las apiladas, uno por serie de la leyenda.",
              "<b>Eje X</b>: deja los nombres y apaga el título. <b>Eje Y</b>: apaga el título; en 100 % apilado el eje ya va de 0 a 100 %.",
              "<b>Leyenda</b>: actívala si hay más de una serie y ponla arriba a la derecha.",
              f"<b>General ▸ Título ▸ Texto</b>: «{esc(v['titulo'])}». Apaga el <b>Subtítulo</b>."]
    elif t == "linea":
        p += ["<b>Líneas ▸ Colores</b>: " + esc("; ".join(colores)) + ". Ancho de línea: 2 a 3 px.",
              "<b>Eje X</b>: apaga el título. <b>Eje Y</b>: apaga el título; fija mínimo y máximo si la línea queda aplastada.",
              "<b>Etiquetas de datos</b>: si salen todas y estorban, apágalas; el último valor ya está en la tarjeta.",
              f"<b>General ▸ Título ▸ Texto</b>: «{esc(v['titulo'])}». Apaga el <b>Subtítulo</b>."]
    elif t == "matriz":
        p += ["<b>Celdas ▸ Color de fondo ▸ fx</b> (formato condicional) ▸ Formato por: Valor del campo ▸ escala de un solo color, del claro al oscuro.",
              "<b>Cuadrícula</b>: horizontal ligera; <b>Totales</b> de filas y columnas: apágalos.",
              f"<b>General ▸ Título ▸ Texto</b>: «{esc(v['titulo'])}»."]
    elif t == "tabla":
        p += ["<b>Cuadrícula</b>: solo líneas horizontales finas. <b>Encabezados de columna</b>: texto en negrita.",
              "<b>Celdas ▸ Valor</b>: tamaño 14 a 16 pt. Alinea las cifras a la derecha.",
              f"<b>General ▸ Título ▸ Texto</b>: «{esc(v['titulo'])}»."]
    return p


def pasos_orden(v):
    """Lo que hay que ordenar y formatear para que las categorías salgan en su posición y los valores como porcentaje o soles."""
    t, u = v["tipo"], v.get("unidad", "")
    p = []
    vistos = set()
    for campo in (v["x"], v.get("serie", "")):
        m = RE_REF.search(campo or "")
        if not m or m.group(2) not in ORDEN_POR or m.groups() in vistos:
            continue
        vistos.add(m.groups())
        tabla, col = m.groups()
        p.append(f"Ordena <b>{esc(tabla)}[{esc(col)}]</b> por la columna <b>{esc(ORDEN_POR[col])}</b>: en el panel Datos selecciona la columna ▸ Herramientas de columna ▸ <b>Ordenar por columna</b> ▸ {esc(ORDEN_POR[col])}. Se hace una vez y vale para todos los visuales.")
    if t == "barras":
        p.append("En el visual, menú «…» arriba a la derecha ▸ <b>Ordenar eje</b> ▸ elige la medida ▸ <b>Orden descendente</b>: la barra más larga queda arriba.")
    elif t == "matriz":
        p.append("En el visual, menú «…» ▸ Ordenar eje ▸ elige el campo de las filas ▸ Orden ascendente. Las columnas siguen el orden de la columna clave de arriba.")
    elif t == "tabla":
        p.append("En el visual, haz clic en el encabezado de la columna <b>kpi</b> para ordenar; con la columna clave KPI-01 a KPI-07 quedan en ese orden.")
    elif any(x in v["x"] for x in ("mes_anio", "dia_semana", "turno")):
        p.append("En el visual, menú «…» ▸ <b>Ordenar eje</b> ▸ elige el campo del eje X ▸ <b>Orden ascendente</b> (así sigue el orden de la columna clave y no el alfabético).")
    elif "fecha" in v["x"]:
        p.append("En el visual, menú «…» ▸ Ordenar eje ▸ fecha ▸ Orden ascendente.")
    med = re.findall(r"\[([^\]]+)\]", v["y"])
    nombre = med[0] if len(med) == 1 else "cada medida"
    fm = formato_medida(u)
    if t != "tabla":
        p.append(f"<b>Formato de la medida</b> (una sola vez): en el panel Datos de la derecha haz clic en la medida <b>[{esc(nombre)}]</b> ▸ en la cinta superior se abre <b>Herramientas de medida</b> ▸ grupo <b>Formato</b> ▸ en la lista desplegable elige "
                 f"<b>{esc(fm.split(',')[0])}</b> ▸ en el cuadro de decimales escribe <b>{'1' if u == '%' else '0' if u == 'S/' else '2' if u == 'S/ por kg' else '0'}</b>. "
                 + ("La medida devuelve una fracción (0.653); el formato Porcentaje la muestra como 65.3 %. Sin este paso el eje sale de 0.0 a 0.7." if u == "%" else ""))
    if t in ("barras", "columnas"):
        pos = "Fuera del extremo (a la derecha de cada barra)" if t == "barras" else "Fuera del extremo (encima de cada columna)"
        p.append(f"<b>Números junto a cada {'barra' if t == 'barras' else 'columna'}</b>: haz clic en el visual ▸ Visualizaciones ▸ pestaña <b>Formato</b> (pincel) ▸ <b>Elementos visuales</b> ▸ <b>Etiquetas de datos</b> ▸ enciende el interruptor ▸ despliega "
                 f"<b>Opciones</b> ▸ <b>Posición</b>: {pos}. En <b>Valor</b>: Unidades de visualización = <b>Ninguna</b> y posiciones decimales = <b>Automático</b> (toma el formato de la medida; sale «65.3 %»).")
        if t == "barras":
            p.append("<b>Quitar la escala de abajo</b> (0 % a 70 %), que ya no hace falta con los números en las barras: Elementos visuales ▸ <b>Eje X</b> ▸ apaga el interruptor, y <b>Cuadrícula</b> ▸ apágala.")
    elif t == "apiladas100":
        p.append("El eje ya va de 0 a 100 %. Para ver el porcentaje dentro de cada tramo: Elementos visuales ▸ Etiquetas de datos ▸ enciende ▸ Posición: Centro.")
    elif t == "linea":
        p.append("Para ver el valor en los puntos: Elementos visuales ▸ <b>Etiquetas de datos</b> ▸ enciende el interruptor; toma el formato de la medida.")
    return p


def seccion_diseno(plan, resp, modelo, metas):
    """Sección aparte con los pasos de diseño (colores, etiquetas, ejes, títulos) de cada visual."""
    cajas = []
    for p_ in plan["paginas"]:
        for v in p_["visuales"]:
            pasos = pasos_diseno(v, datos_visual(v, resp, modelo, metas), v.get("unidad", ""))
            cajas.append(f'<div class="caja" id="d-{p_["codigo"]}-{v["id"]}"><h4><span class="cod">{esc(p_["codigo"])}</span><span class="num">{v["id"]}</span> {esc(v["titulo"])}</h4>'
                         f'<p class="cm">Diseño: {esc(NOMBRE_TIPO[v["tipo"]])}</p><ol class="pasos">' + "".join(f"<li>{x}</li>" for x in pasos) + "</ol></div>")
    return ('<section class="final" id="diseno"><h2>Diseño de los gráficos</h2><p class="preg">Esto es presentación (colores, etiquetas, títulos y ejes). '
            'Hazlo al final, cuando los datos, el orden y los porcentajes ya salgan bien.</p>'
            f'<div class="cajas">{"".join(cajas)}</div></section>')


def caja_construir(v, plan, resp, modelo, metas, pc=""):
    en_y = {n for n in re.findall(r"\[([^\]]+)\]", v["y"])}
    por = {m["codigo"]: m for m in plan["medidas"]}
    cod_y = [c for c in v["medidas"] if c in por and por[c]["nombre"] in en_y]
    cod_otras = [c for c in v["medidas"] if c in por and c not in cod_y]
    t = v["tipo"]
    barras = t == "barras"  # en barras horizontales los ejes van al revés: categorías en Eje Y y la medida en Eje X
    campos = [("Tipo de visual", esc(NOMBRE_TIPO[t]) + " (panel Visualizaciones)"),
              (("Eje Y (categorías)" if barras else "Eje X / filas") if t != "matriz" else "Filas", campo_eje_html(v["x"]))]
    if v["serie"]:
        campos.append(("Columnas" if t == "matriz" else "Leyenda", campo_eje_html(v["serie"])))
    campos.append((("Eje X (valores)" if barras else "Valores (eje Y)") if t != "matriz" else "Valores", medidas_html(plan, v, cod_y) or esc(v["y"])))
    if cod_otras:
        campos.append(("Otras medidas del visual", medidas_html(plan, v, cod_otras)))
    if t == "tabla":
        campos = [c for c in campos if not c[0].startswith("Valores")]
        campos.append(("Columnas de la tabla (DAX)", "<span class='med'><span>No arrastres las 7 medidas: cada una repetiría su valor en las 7 filas. Usa estas 4 (la primera es solo de apoyo y no se arrastra; vienen en la sección «Medidas DAX de las tarjetas y chips»):</span></span>"
                       + "".join(dax_bloque(*x) for x in DAX_TABLA[0:4]) + "<span class='med'><span>El campo <b>dKpi[kpi]</b> va en Columnas; después arrastra, en este orden: [Valor del KPI], [Meta del KPI (texto)], [Estado del KPI]. Para el color del chip: [Estado del KPI] ▸ Formato condicional ▸ Color de fuente ▸ Valor del campo ▸ [Color del estado].</span></span>"))
    campos.append(("Filtros del visual", esc("; ".join(v["filtros"]))))
    campos.append(("Orden, porcentajes y etiquetas (para que salga en su posición)", "<ol class='pasos'>" + "".join(f"<li>{x}</li>" for x in pasos_orden(v)) + "</ol>"))
    campos.append(("Archivos CSV de origen", ", ".join(f"<code>{esc(_csv_de(o))}</code>" for o in v["origen"])))
    campos.append(("Valor esperado", esc(esperado_resumen(v, resp, modelo, metas))))
    dl = "".join(f"<dt>{esc(a)}</dt><dd>{b}</dd>" for a, b in campos)
    return (f'<div class="caja" id="c-{pc}-{v["id"]}"><h4><span class="num">{v["id"]}</span> {esc(v["titulo"])}</h4><p class="cm">Cómo construirlo en Power BI</p><dl>{dl}</dl>'
            f'<p class="fmt">{esc(v.get("formato", ""))}</p></div>')


def caja_segmentadores(p):
    filas = []
    for s_ in p.get("segmentadores", []):
        m = RE_REF.search(s_)
        if not m:
            continue
        tabla, col = m.groups()
        orden = f" Ordénala por <b>{ORDEN_POR[col]}</b>." if col in ORDEN_POR else ""
        filas.append(f"<dt>{esc(s_)}</dt><dd>Segmentación de datos: arrastra la columna {_ref_html(tabla, col)} al campo <b>Campo</b> (archivo <code>{esc(_csv_de(tabla))}</code>).{orden}</dd>")
    if not filas:
        return ""
    return (f'<div class="caja" id="c-{p["codigo"]}-seg"><h4>Segmentadores (filtros de la página)</h4><p class="cm">Cómo construirlos en Power BI</p><dl>' + "".join(filas) + "</dl>"
            '<p class="fmt">Cada uno es un visual «Segmentación de datos» en la franja superior derecha. En Vista ▸ Sincronizar segmentadores activa la sincronización con las demás páginas.</p></div>')


COLOR_OK, COLOR_MAL, COLOR_SIN = "#0F7B3F", "#B3261E", "#6B7280"
MES_REF = ("Mes de referencia",
           "LOOKUPVALUE ( dCalendario[mes_anio], dCalendario[fecha], MAX ( dCalendario[fecha] ) )",
           "Texto del último mes que deja pasar el filtro («oct 26»). Va en el subtítulo de cada tarjeta.")


def _num_kpi(k):
    return int(k[-2:])


def dax_tarjeta(k, plan, metas):
    """[(nombre, dax, explicación)] de las tres medidas de texto de una tarjeta: meta, estado (chip) y color del chip."""
    m = metas[k]
    n = _num_kpi(k)
    med = next(x for x in plan["medidas"] if x["kpi"] == k)
    op = "<=" if m["cmp"] == "<=" else ">="
    sent = "o menos" if m["cmp"] == "<=" else "o más"
    meta = f"CALCULATE ( AVERAGE ( fMetaKpi[meta] ), dKpi[kpi_key] = {n} )"
    return [
        (f"Meta texto {k}",
         f"VAR meta = {meta}\nRETURN\n    \"Meta: \" & IF ( ISBLANK ( meta ), \"Pendiente\", FORMAT ( meta, \"0\" ) & \" % {sent}\" ) & \" · \" & [Mes de referencia]",
         f"Subtítulo de la tarjeta de {k}: «Meta: {m['meta_texto']} · mes». La meta sale de fMetaKpi[meta], no está escrita a mano."),
        (f"Estado {k}",
         f"VAR valor = [{med['nombre']}]\nVAR meta = {meta} / 100\nRETURN\n    IF ( ISBLANK ( meta ), \"– Sin meta\", IF ( valor {op} meta, \"✔ Cumple\", \"✖ No cumple\" ) )",
         f"Texto del chip de {k}. Cumple si el valor es {'menor o igual' if op == '<=' else 'mayor o igual'} a la meta; sin meta muestra «– Sin meta». Se divide entre 100 porque la meta se guarda como 12 y la medida devuelve 0.12."),
        (f"Color estado {k}",
         f"SWITCH ( LEFT ( [Estado {k}], 1 ), \"✔\", \"{COLOR_OK}\", \"✖\", \"{COLOR_MAL}\", \"{COLOR_SIN}\" )",
         f"Color del chip de {k} (verde, rojo o gris). Se usa en Formato condicional ▸ Valor del campo."),
    ]


DAX_TABLA = [
    ("Valor numérico del KPI",
     "SWITCH (\n    SELECTEDVALUE ( dKpi[kpi_key] ),\n    1, [Calidad de datos %],\n    2, [Margen de contribución %],\n    3, [Margen neto %],\n    4, [Merma %],\n    5, [Error del pronóstico %],\n    6, [Precio promedio del pollo vivo],\n    7, CALCULATE ( [KPI con meta %], ALL ( dKpi ) )\n)",
     "Devuelve el valor del KPI de cada fila. El KPI-07 usa ALL(dKpi) porque cuenta todos los KPI y no solo el de la fila."),
    ("Valor del KPI",
     "VAR v = [Valor numérico del KPI]\nRETURN\n    IF ( SELECTEDVALUE ( dKpi[kpi_key] ) = 6, \"S/ \" & FORMAT ( v, \"0.00\" ), FORMAT ( v, \"0.0 %\" ) )",
     "El mismo valor, ya como texto con su unidad (% o S/)."),
    ("Meta del KPI (texto)",
     "VAR k = SELECTEDVALUE ( dKpi[kpi_key] )\nVAR meta = AVERAGE ( fMetaKpi[meta] )\nRETURN\n    IF ( ISBLANK ( meta ), \"Pendiente\", FORMAT ( meta, \"0\" ) & \" % \" & IF ( k IN { 4, 5 }, \"o menos\", \"o más\" ) )",
     "Meta de la fila, con el sentido (o más / o menos). KPI-04 y KPI-05 son «o menos»."),
    ("Estado del KPI",
     "VAR k = SELECTEDVALUE ( dKpi[kpi_key] )\nVAR valor = [Valor numérico del KPI]\nVAR meta = AVERAGE ( fMetaKpi[meta] ) / 100\nRETURN\n    IF (\n        ISBLANK ( meta ), \"– Sin meta\",\n        IF ( IF ( k IN { 4, 5 }, valor <= meta, valor >= meta ), \"✔ Cumple\", \"✖ No cumple\" )\n    )",
     "Chip de cada fila de la tabla."),
    ("Color del estado",
     f"SWITCH ( LEFT ( [Estado del KPI], 1 ), \"✔\", \"{COLOR_OK}\", \"✖\", \"{COLOR_MAL}\", \"{COLOR_SIN}\" )",
     "Color del chip de la tabla."),
]


def dax_bloque(nombre, dax, nota=""):
    return (f'<div class="med"><b>[{esc(nombre)}]</b> · medida DAX, créala en la tabla <b>Medidas</b><code>{esc(nombre)} =\n{esc(dax)}</code>'
            f'{"<span>" + esc(nota) + "</span>" if nota else ""}</div>')


def caja_tarjeta(k, plan, metas, pc=""):
    m = metas[k]
    med = next((x for x in plan["medidas"] if x["kpi"] == k), None)
    campos = [("Tipo de visual", "Tarjeta (la nueva, no la «clásica»): panel Visualizaciones ▸ Tarjeta")]
    if med:
        campos.append(("Valor grande (DAX)", medidas_html(plan, {}, [med["codigo"]])))
    if med:
        mt, est, col = dax_tarjeta(k, plan, metas)
        campos.append(("Texto de meta (DAX)", dax_bloque(*mt)))
        campos.append(("Chip de estado (DAX)", dax_bloque(*est)))
        campos.append(("Color del chip (DAX)", dax_bloque(*col)))
        campos.append(("Mes de referencia (DAX)", dax_bloque(*MES_REF) + "<span>Es la misma para todas las tarjetas: créala una vez.</span>"))
    pasos = [
        f"Arrastra <b>[{esc(med['nombre'] if med else k)}]</b> al campo <b>Campo</b> de la tarjeta: es el número grande.",
        f"Formato de la medida: Herramientas de medida ▸ Formato ▸ {'Moneda, 2 decimales' if k == 'KPI-06' else 'Porcentaje, 1 decimal'} (si no, sale 0.08 en vez de 8.0 %).",
        f"<b>Chip:</b> en Visualizaciones ▸ Formato ▸ Elementos visuales ▸ <b>Etiquetas de referencia</b> ▸ enciéndelas ▸ <b>Valor</b>: arrastra <b>[Estado {k}]</b>. "
        "Si tu versión no tiene Etiquetas de referencia, pon una segunda tarjeta pequeña con esa medida pegada a la primera.",
        f"<b>Color del chip:</b> en esa misma etiqueta, color del texto ▸ <b>fx</b> ▸ Formato por: <b>Valor del campo</b> ▸ campo: <b>[Color estado {k}]</b>.",
        f"<b>Subtítulo de meta:</b> en la etiqueta de referencia ▸ <b>Detalle</b>: arrastra <b>[Meta texto {k}]</b>; sale «Meta: {esc(m['meta_texto'])} · oct 26».",
        "<b>Título:</b> General ▸ Título ▸ Texto: el nombre del KPI.",
    ]
    campos.append(("Cómo armarla (clics)", "<ol class='pasos'>" + "".join(f"<li>{x}</li>" for x in pasos) + "</ol>"))
    campos.append(("Filtro del visual (clics)", "Panel Filtros ▸ arrastra <b>dCalendario[mes_anio]</b> a «Filtros en este objeto visual» ▸ Tipo de filtro: <b>N superior</b> ▸ Mostrar elementos: <b>Superior 1</b> ▸ Por valor: arrastra <b>dCalendario[anio_mes]</b> (Máximo) ▸ Aplicar filtro. "
                                              "Así la tarjeta siempre muestra el último mes sin escribir «oct 26»."))
    dl = "".join(f"<dt>{esc(a)}</dt><dd>{b}</dd>" for a, b in campos)
    return f'<div class="caja" id="c-{pc}-{k}"><h4><span class="cod">{esc(k)}</span> {esc(m["nombre"])}</h4><p class="cm">Cómo construir la tarjeta en Power BI</p><dl>{dl}</dl></div>'


def seccion_medidas_tarjetas(plan, metas):
    """Las medidas de texto (meta, chip y color) de las tarjetas y de la tabla de KPI, en el orden de creación."""
    cajas = [dax_bloque(*MES_REF)]
    out = [("Mes de referencia", "tarjetas", MES_REF)]
    for p in plan["paginas"]:
        for k in p.get("kpis", []):
            if any(x["kpi"] == k for x in plan["medidas"]):
                for t in dax_tarjeta(k, plan, metas):
                    out.append((t[0], f"{p['codigo']} · tarjeta {k}", t))
    if any(v["tipo"] == "tabla" for p in plan["paginas"] for v in p["visuales"]):
        for t in DAX_TABLA:
            out.append((t[0], "tabla de KPI", t))
    vistos, filas = set(), []
    for n, (nombre, uso, (nom, dax, expl)) in enumerate(out, 1):
        if nombre in vistos:
            continue
        vistos.add(nombre)
        filas.append(f'<div class="caja"><h4><span class="num">{len(filas) + 1}</span> [{esc(nom)}]</h4><p class="cm">Texto o color · medida DAX</p>'
                     f'<p class="fmt" style="margin:0 0 6px">{esc(expl)}</p>{dax_bloque(nom, dax)}<p class="fmt">Se usa en: {esc(uso)}.</p></div>')
    return ('<section class="final" id="medidas-tarjetas"><h2>Medidas DAX de las tarjetas y chips</h2><p class="preg">Son medidas de texto y de color. Créalas después de las medidas globales, en este orden, '
            'en la misma tabla <b>Medidas</b>. Lo que no es DAX (arrastrar, filtros y formato) está en la caja de cada tarjeta.</p>'
            f'<div class="cajas">{"".join(filas)}</div></section>')


# ------------------------------------------------------------------ HTML completo
CSS = """
*{box-sizing:border-box}body{margin:0;background:var(--c-fondo);color:var(--c-texto);font-family:var(--fuente);font-size:16px;line-height:1.45}
.barra{position:sticky;top:0;z-index:5;display:flex;gap:16px;align-items:center;padding:12px 24px;background:var(--c-superficie);border-bottom:1px solid var(--c-borde)}
.barra h1{font-size:20px;margin:0;font-weight:700}.barra .sub{color:var(--c-texto-secundario);font-size:14px}.barra button{margin-left:auto;font:inherit;font-size:14px;padding:6px 14px;border-radius:12px;border:1px solid var(--c-borde);background:var(--c-fondo);color:var(--c-texto);cursor:pointer}
main{padding:24px;max-width:1650px;margin:0 auto}.pagina{margin:0 0 56px}.pagina>h2{font-size:26px;margin:0 0 4px;font-weight:700}.pagina>.preg{color:var(--c-texto-secundario);margin:0 0 14px}
.lienzo{width:1600px;height:900px;padding:24px;background:var(--c-superficie);border:1px solid var(--c-borde);border-radius:20px;display:flex;flex-direction:column;gap:16px;overflow:hidden}
.enc{height:76px;display:flex;align-items:center;gap:20px;flex:none}.enc h3{margin:0;font-size:26px;font-weight:700}.enc .quien{color:var(--c-texto-secundario);font-size:16px}
.seg{margin-left:auto;display:flex;gap:10px}.seg span{border:1px solid var(--c-borde);background:var(--c-fondo);border-radius:12px;padding:6px 14px;font-size:16px;color:var(--c-texto-secundario)}
.tarjetas.muchas .t-valor{font-size:28px;white-space:nowrap}.tarjetas.muchas .tarjeta{padding:10px 12px}.tarjetas.muchas .chip{font-size:13px;padding:2px 8px}.tarjetas.muchas .t-etq{font-size:14px}.tarjetas{height:120px;display:flex;gap:16px;flex:none}.tarjeta{flex:0 1 calc((100% - 64px) / 5);background:var(--c-fondo);border:1px solid var(--c-borde);border-radius:16px;padding:10px 18px;gap:4px;display:flex;flex-direction:column;justify-content:space-between;min-width:0}
.t-etq{font-size:16px;color:var(--c-texto-secundario);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.t-valor{font-size:36px;font-weight:700;line-height:1}.t-fila{display:flex;justify-content:space-between;align-items:center;gap:8px}.t-meta{font-size:14px;color:var(--c-texto-secundario);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cod{font-family:var(--fuente-mono,ui-monospace,monospace);font-size:14px;color:var(--c-texto-secundario)}
.chip{white-space:nowrap;display:inline-flex;gap:6px;align-items:center;border-radius:999px;padding:2px 12px;font-size:14px;font-weight:600;border:1px solid currentColor}.chip.ok{color:var(--c-exito)}.chip.mal{color:var(--c-error)}.chip.sin{color:var(--c-texto-secundario)}
.zona{flex:1;display:grid;grid-template-columns:repeat(12,1fr);gap:16px;min-height:0}
.visual{margin:0;background:var(--c-fondo);border:1px solid var(--c-borde);border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;min-width:0;min-height:0;overflow:hidden}
.visual figcaption{display:flex;align-items:center;gap:10px;height:38px;flex:none}.v-titulo{font-size:18px;font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.num{display:inline-flex;align-items:center;justify-content:center;min-width:24px;height:24px;border-radius:12px;background:var(--c-acento);color:var(--c-acento-texto);font-size:14px;font-weight:700;flex:none}
.leyenda{margin-left:auto;display:flex;gap:14px;font-size:14px;color:var(--c-texto-secundario);white-space:nowrap}.leyenda i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.k-meta{background:none!important;border-top:2px dashed var(--c-texto-secundario);height:0!important;width:18px!important;border-radius:0!important;vertical-align:4px!important}.k-marca{border:2.5px solid var(--c-serie-4);border-radius:50%!important;background:var(--c-superficie)!important;width:10px!important;height:10px!important}
.cuerpo{flex:1;min-height:0;position:relative}.cuerpo svg{display:block}
.eje{fill:var(--c-texto-secundario)}.cat{fill:var(--c-texto)}.valor{fill:var(--c-texto);font-weight:600}.rejilla{stroke:var(--c-borde);stroke-width:1}.meta{stroke:var(--c-texto-secundario);stroke-width:1.5;stroke-dasharray:6 5}.etq-meta{fill:var(--c-texto-secundario);font-weight:600}.cruz{stroke:var(--c-texto-secundario);stroke-width:1;opacity:.6}
table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.2}th,td{padding:6px 10px;text-align:left;border-bottom:1px solid var(--c-borde)}th{color:var(--c-texto-secundario);font-weight:600}td.der,th.der{text-align:right}
.matriz td,.matriz th{padding:3px 10px}.matriz td{text-align:center;font-weight:600}.matriz th:first-child{text-align:left}.tkpi td,.tkpi th{padding:3px 10px}
.pagina>.cajas{display:none}.cajas{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px;margin-top:20px;max-width:1600px}.caja{background:var(--c-superficie);border:1px solid var(--c-borde);border-radius:16px;padding:14px 18px}.caja h4{margin:0;font-size:18px;display:flex;gap:8px;align-items:center}.cm{margin:2px 0 8px;color:var(--c-acento-fuerte);font-weight:700;font-size:14px;text-transform:none}
dl{margin:0;display:grid;grid-template-columns:130px 1fr;gap:4px 12px;font-size:15px}.med{margin:0 0 8px}.med code{display:block;margin:3px 0;padding:6px 8px;border-radius:8px;background:var(--c-fondo);border:1px solid var(--c-borde);font-size:13px;white-space:pre-wrap}.visual[data-caja],.tarjeta[data-caja],.seg[data-caja]{cursor:pointer;transition:box-shadow .15s,border-color .15s}.visual[data-caja]:hover,.tarjeta[data-caja]:hover,.seg[data-caja]:hover,.visual[data-caja]:focus-visible,.tarjeta[data-caja]:focus-visible,.seg[data-caja]:focus-visible{border-color:var(--c-acento);box-shadow:0 0 0 2px var(--c-acento);outline:none}
dialog#det{width:min(920px,94vw);max-height:90vh;padding:0;border:1px solid var(--c-borde);border-radius:20px;background:var(--c-superficie);color:var(--c-texto);box-shadow:0 20px 60px rgba(0,0,0,.45);overflow:auto}dialog#det::backdrop{background:rgba(0,0,0,.6)}
.det-cab{position:sticky;top:0;z-index:2;display:flex;align-items:center;gap:12px;padding:14px 22px;background:var(--c-superficie);border-bottom:1px solid var(--c-borde)}.det-cab h3{margin:0;font-size:20px}.det-cab button{margin-left:auto;font:inherit;font-size:15px;padding:6px 16px;border-radius:12px;border:1px solid var(--c-borde);background:var(--c-fondo);color:var(--c-texto);cursor:pointer}
.det-cuerpo{padding:8px 22px 22px}.det-cuerpo .caja{border:0;padding:12px 0;border-bottom:1px solid var(--c-borde);border-radius:0}.det-cuerpo .caja:last-child{border-bottom:0}.det-cuerpo dl{grid-template-columns:190px 1fr;font-size:16px}.det-cuerpo .med code{font-size:14px}
.pasos{margin:0;padding-left:18px}.pasos li{margin:0 0 4px}.med span{color:var(--c-texto-secundario);font-size:13px}dd code{font-size:13px}dt{color:var(--c-texto-secundario);word-break:break-word;min-width:0}dd{margin:0;word-break:break-word;min-width:0}.fmt{margin:8px 0 0;color:var(--c-texto-secundario);font-size:14px}
.final{max-width:1600px}.final h2{font-size:26px}.scroll{overflow-x:auto;background:var(--c-superficie);border:1px solid var(--c-borde);border-radius:16px;padding:8px}.scroll td,.scroll th{white-space:nowrap;font-size:15px}
#tip{position:fixed;display:none;pointer-events:none;z-index:9;background:var(--c-superficie);color:var(--c-texto);border:1px solid var(--c-borde);border-radius:10px;padding:8px 12px;font-size:15px;box-shadow:var(--sombra-md,0 6px 20px rgba(0,0,0,.25))}
"""

JS = """
try{var q=/[?&]tema=(light|dark)/.exec(location.search),g=q?q[1]:localStorage.getItem("tema"),d=getComputedStyle(document.documentElement).getPropertyValue("--tema-defecto").trim()==="oscuro"?"dark":"light";document.documentElement.setAttribute("data-theme",g==="dark"||g==="light"?g:d)}catch(e){}
document.addEventListener("DOMContentLoaded",function(){
var t=document.getElementById("tip"),pg=/[?&]pag=([\\w-]+)/.exec(location.search);
if(pg)document.querySelectorAll(".pagina,.final").forEach(function(e){if(e.id!==pg[1])e.style.display="none"});
document.addEventListener("mousemove",function(e){var el=e.target.closest&&e.target.closest("[data-tip]");
document.querySelectorAll(".cruz").forEach(function(c){c.setAttribute("x1",-10);c.setAttribute("x2",-10)});
if(!el){t.style.display="none";return}
t.innerHTML=el.getAttribute("data-tip");t.style.display="block";t.style.left=Math.min(e.clientX+14,window.innerWidth-260)+"px";t.style.top=(e.clientY+14)+"px";
var x=el.getAttribute("data-x"),s=el.closest("svg"),c=s&&s.querySelector(".cruz");if(x&&c){c.setAttribute("x1",x);c.setAttribute("x2",x)}});
var dlg=document.getElementById("det");
function abrir(el){var id=el.getAttribute("data-caja"),a=document.getElementById("c-"+id),d=document.getElementById("d-"+id);if(!a)return;
var tit=a.querySelector("h4").textContent.replace(/\\s+/g," ").trim(),h="";
h+=a.outerHTML.replace(/ id="[^"]*"/,"");
if(d)h+=d.outerHTML.replace(/ id="[^"]*"/,"");
dlg.innerHTML='<div class="det-cab"><h3>'+tit+'</h3><button type="button" id="det-x">Cerrar</button></div><div class="det-cuerpo">'+h+'</div>';
dlg.querySelector("h4").remove();
if(d){var cs=dlg.querySelectorAll(".caja");if(cs[1]){var h4=cs[1].querySelector("h4");if(h4)h4.remove()}}
dlg.querySelector("#det-x").addEventListener("click",function(){dlg.close()});dlg.showModal();dlg.scrollTop=0}
document.addEventListener("click",function(e){var el=e.target.closest&&e.target.closest("[data-caja]");if(el){abrir(el);return}if(e.target===dlg)dlg.close()});
document.addEventListener("keydown",function(e){if((e.key==="Enter"||e.key===" ")&&e.target.getAttribute&&e.target.getAttribute("data-caja")){e.preventDefault();abrir(e.target)}});
document.getElementById("tema").addEventListener("click",function(){var h=document.documentElement,n=h.getAttribute("data-theme")==="dark"?"light":"dark";h.setAttribute("data-theme",n);try{localStorage.setItem("tema",n)}catch(e){}});
});
"""


def html_referencia(plan, resp, modelo, metas, brief, tokens):
    paginas = []
    for p in plan["paginas"]:
        tarj = "".join(html_tarjeta(valor_kpi(resp, k, metas)).replace('<div class="tarjeta">', f'<div class="tarjeta" data-caja="{p["codigo"]}-{k}" tabindex="0" role="button" title="Clic para ver cómo construirla">', 1) for k in p.get("kpis", []))
        seg = "".join(f"<span>{esc(s)}</span>" for s in p.get("segmentadores", []))
        vis = "".join(render_visual(v, p, resp, modelo, metas) for v in p["visuales"])
        cajas = caja_segmentadores(p) + "".join(caja_tarjeta(k, plan, metas, p["codigo"]) for k in p.get("kpis", [])) + "".join(caja_construir(v, plan, resp, modelo, metas, p["codigo"]) for v in p["visuales"])
        paginas.append(
            f'<section class="pagina" id="{esc(p["codigo"])}"><h2><span class="cod">{esc(p["codigo"])}</span> {esc(p["nombre"])}</h2>'
            f'<p class="preg">Para el {esc(p["usuario"].lower())}: {esc(p["pregunta"])}</p>'
            f'<div class="lienzo"><div class="enc"><h3>{esc(p["nombre"])}</h3><span class="quien">{esc(p["usuario"])}</span><div class="seg" data-caja="{esc(p["codigo"])}-seg" tabindex="0" role="button" title="Clic para ver cómo construir los filtros">{seg}</div></div>'
            f'{f"<div class='tarjetas{' muchas' if len(p.get('kpis', [])) > 5 else ''}'>{tarj}</div>" if tarj else ""}<div class="zona">{vis}</div></div>'
            f'<div class="cajas">{cajas}</div></section>')
    kpis = sorted({r["kpi"] for r in resp["kpi-esperados"]})
    meses = sorted({r["mes"] for r in resp["kpi-esperados"]})
    por = {(r["kpi"], r["mes"]): r for r in resp["kpi-esperados"]}
    cab = "".join(f"<th class='der'>{esc(etiqueta_mes(m))}</th>" for m in meses)
    filas = []
    for k in kpis:
        u = "S/ por kg" if k == "KPI-06" else "%"
        celdas = "".join(f"<td class='der'>{fmt(float(por[(k, m)]['valor']), u) if (k, m) in por and por[(k, m)]['valor'] != '' else '—'}</td>" for m in meses)
        filas.append(f"<tr><td class='cod'>{k}</td><td>{esc(metas[k]['nombre'])}</td><td>{esc(metas[k]['meta_texto'])}</td>{celdas}</tr>")
    diseno = seccion_medidas_tarjetas(plan, metas) + seccion_diseno(plan, resp, modelo, metas)
    final = (diseno + f'<section class="final" id="valores"><h2>Valores esperados por mes</h2><p class="preg">Son los de la hoja de respuestas (data/respuestas/kpi-esperados.csv). '
             f'Tu dashboard debería dar valores muy cercanos; el pronóstico (KPI-05) usa un método simple y el de Power BI no coincidirá exactamente.</p>'
             f'<div class="scroll"><table><thead><tr><th>Código</th><th>KPI</th><th>Meta</th>{cab}</tr></thead><tbody>{"".join(filas)}</tbody></table></div></section>')
    css = H.tokens_css(tokens)
    titulo = f"Dashboard de referencia · {brief.get('empresa') or brief.get('nombre') or 'proyecto'}"
    return (f'<!doctype html>\n<html lang="es" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{esc(titulo)}</title><style>\n{H.INI}\n{css}\n{H.FIN}\n</style><style>{CSS}</style><script>{JS}</script></head><body>"
            f'<div class="barra"><h1>Dashboard de referencia</h1><span class="sub">Así debería verse y estos son los valores esperados. Se construye en Power BI. Haz clic en un gráfico, tarjeta o filtro para ver cómo construirlo.</span>'
            f'<button id="tema" type="button">Tema claro / oscuro</button></div><main>{"".join(paginas)}{final}</main><div id="tip"></div><dialog id="det"></dialog></body></html>\n')


# ------------------------------------------------------------------ guía en Markdown
def _tabla(cab, filas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in f) + " |" for f in filas]
    return out


def pasos_visual(v, plan):
    """Pasos concretos en Power BI para armar un visual."""
    t, u = v["tipo"], v.get("unidad", "")
    meds = ", ".join(nombres_medidas(plan, v["medidas"]))
    p = []
    inserta = {"linea": "Gráfico de líneas", "columnas": "Gráfico de columnas agrupadas", "apiladas": "Gráfico de columnas apiladas", "apiladas100": "Gráfico de columnas apiladas al 100 %",
               "barras": "Gráfico de barras agrupadas", "matriz": "Matriz", "tabla": "Tabla", "tarjeta": "Tarjeta"}[t]
    p.append(f"En el panel Visualizaciones elige **{inserta}** y colócalo en la posición indicada en el HTML de referencia (visual {v['id']}).")
    if t == "matriz":
        p.append(f"Arrastra a **Filas** {v['x']}; a **Columnas** {v['serie']}; y a **Valores** {v['y']}.")
    elif t == "tabla":
        p.append(f"Arrastra a **Columnas** {v['x']} y cada medida de la lista: {meds}.")
    else:
        if t == "barras":
            p.append(f"Arrastra a **Eje Y** {v['x']} (en las barras horizontales las categorías van en el eje Y y la medida en el eje X; si lo pones al revés, Power BI dice que el campo no es una medida).")
        else:
            p.append(f"Arrastra a **Eje X** {v['x']}.")
        orden = re.match(r"(\w+\[\w+\]) \(ordenada por (\w+\[(\w+)\])\)", v["x"])
        if orden:
            p.append(f"Si los valores salen en orden alfabético, selecciona `{orden.group(1)}` en el panel Datos y ve a Herramientas de columna ▸ **Ordenar por columna** ▸ `{orden.group(3)}`.")
        eje_medida = "Eje X" if t == "barras" else "Eje Y"
        p.append(f"Arrastra a **{eje_medida}** {v['y']}." if v["y"].count("[") == 1 else f"Arrastra a **{eje_medida}** las medidas: {v['y']}.")
        if v.get("serie") and v["serie"].startswith("dCanal"):
            p.append(f"Arrastra a **Leyenda** {v['serie']}.")
    for f in v["filtros"]:
        if not f.lower().startswith(("ninguno", "todo")):
            p.append(f"En el panel Filtros de este visual aplica: {f}.")
    if v.get("meta"):
        p.append("En el panel **Analytics** agrega una **Línea constante** en el valor de la meta (la medida «Meta del KPI» o el valor de la sección 2.5) y rotúlala.")
    if t in ("linea", "columnas", "apiladas", "apiladas100"):
        p.append("En Formato: activa la leyenda si hay más de una serie, deja las etiquetas de datos solo en lo necesario y pon el título del visual.")
    if v.get("formato"):
        p.append(v["formato"])
    return p


def filas_ventas(resp):
    """Filas leídas de las cuatro fuentes de ventas, con el separador de miles."""
    n = sum(int(r["filas_brutas"]) for r in resp.get("filas-por-fuente", []) if r["fuente"] in ("fue-01", "fue-02", "fue-03", "fue-04"))
    return f"{n:,}".replace(",", ESPACIO)


RE_MEDIDA = re.compile(r"(?<![\w\]])\[([^\]]+)\]")
RE_COLUMNA = re.compile(r"\b([A-Za-z_]\w*)\[([^\]]+)\]")


def _medida_de_kpi(plan, kpi):
    return next((m for m in plan["medidas"] if m["kpi"] == kpi), None)


class _Guia:
    """Lleva la cuenta de lo ya explicado para que cada medida y cada columna calculada se explique en el primer elemento que la usa."""

    def __init__(self, plan, resp, modelo, metas):
        self.plan, self.resp, self.modelo, self.metas = plan, resp, modelo, metas
        self.por_codigo = {m["codigo"]: m for m in plan["medidas"]}
        self.por_nombre = {m["nombre"]: m for m in plan["medidas"]}
        self.cols = {(c["tabla"], c["columna"]): c for c in plan["columnas_calculadas"]}
        self.medidas_creadas, self.cols_creadas = {}, {}
        self.donde = ""

    def _orden(self, m, salida):
        """La medida y las que usa, las usadas primero."""
        if m["codigo"] in self.medidas_creadas or m["codigo"] in [x["codigo"] for x in salida]:
            return
        for n in RE_MEDIDA.findall(m["dax"]):
            d = self.por_nombre.get(n)
            if d and d["codigo"] != m["codigo"]:
                self._orden(d, salida)
        salida.append(m)

    def recursivas(self, codigos):
        """Las medidas pedidas y todas las que usan, ya estén creadas o no (para saber de qué columnas salen)."""
        salida, vistos = [], set()

        def ir(m):
            if m["codigo"] in vistos:
                return
            vistos.add(m["codigo"])
            for n in RE_MEDIDA.findall(m["dax"]):
                d = self.por_nombre.get(n)
                if d:
                    ir(d)
            salida.append(m)
        for c in codigos:
            if c in self.por_codigo:
                ir(self.por_codigo[c])
        return salida

    def medidas_nuevas(self, codigos):
        salida = []
        for c in codigos:
            if c in self.por_codigo:
                self._orden(self.por_codigo[c], salida)
        return salida

    def columnas(self, medidas, extra_texto=()):
        """[(tabla, columna)] que usan las medidas (y los ejes), en orden de aparición."""
        vistos, out = set(), []
        for t in [m["dax"] for m in medidas] + list(extra_texto):
            for tabla, col in RE_COLUMNA.findall(t):
                col = re.sub(r"\s*\(.*$", "", col)
                if (tabla, col) not in vistos and (tabla.startswith(("f", "d"))):
                    vistos.add((tabla, col))
                    out.append((tabla, col))
        return out

    def tabla_columnas(self, cols, medidas_usadas):
        filas = []
        for tabla, col in cols:
            c = self.cols.get((tabla, col))
            if c and (tabla, col) not in self.cols_creadas:
                self.cols_creadas[(tabla, col)] = self.donde
                orig = "; ".join(f"`{x}`" for x in c["archivos"])
                filas.append([f"`{tabla}[{col}]`", f"**Columna calculada** ({c['donde']}). {c['formula']}", f"Campos: {'; '.join(f'`{x}`' for x in c['campos'])}. Archivos: {orig}. {c['explicacion']}"])
            elif c:
                filas.append([f"`{tabla}[{col}]`", "Columna calculada", f"Ya la creaste en {self.cols_creadas[(tabla, col)]}"])
            else:
                filas.append([f"`{tabla}[{col}]`", "Columna del modelo", "Viene del ETL (guía de ETL, PAS-10 a PAS-14)"])
        for m in medidas_usadas:
            if m["codigo"] in self.medidas_creadas and self.medidas_creadas[m["codigo"]] != self.donde:
                filas.append([f"[{m['nombre']}]", "Medida", f"Ya la creaste en {self.medidas_creadas[m['codigo']]}"])
        return filas

    def bloque_medidas(self, nuevas):
        out = []
        for m in nuevas:
            self.medidas_creadas[m["codigo"]] = self.donde
            kp = f" ({m['kpi']})" if m["kpi"] else ""
            meta = f" Meta: {self.metas[m['kpi']]['meta_texto']}." if m["kpi"] and m["kpi"] in self.metas else ""
            out += [f"- **{m['codigo']}** · **Medida `{m['nombre']}`**{kp}: {m['explicacion']}{meta} Tablas: {', '.join(f'`{t}`' for t in m['tablas'])}.", "",
                    "```dax", f"{m['nombre']} =", m["dax"], "```", ""]
        return out


def _tarjeta(g, p, k, n):
    """Elemento de una tarjeta de KPI."""
    m = g.metas[k]
    med = _medida_de_kpi(g.plan, k)
    val = valor_kpi(g.resp, k, g.metas)
    g.donde = f"{p['codigo']} · Elemento {n}"
    nuevas = g.medidas_nuevas([med["codigo"]]) if med else []
    cols = g.columnas(g.recursivas([med["codigo"]] if med else []))
    L = [f"### Elemento {n} · Tarjeta {k} · {m['nombre']}", "",
         f"**Qué muestra.** El valor del indicador {k} para el periodo que filtres, con su meta ({m['meta_texto']}) y un estado: Cumple, No cumple o Sin meta.", "",
         f"**Cómo se calcula.** {med['explicacion'] if med else 'Se calcula con la medida del indicador.'}", ""]
    usadas = []
    for x in RE_MEDIDA.findall(med["dax"]) if med else []:
        if x in g.por_nombre and g.por_nombre[x] not in usadas:
            usadas.append(g.por_nombre[x])
    filas = g.tabla_columnas(cols, usadas)
    if filas:
        L += ["**Tablas y columnas.**", ""] + _tabla(["Campo", "Qué es", "De dónde sale"], filas) + [""]
    if nuevas:
        L += ["**Fórmula.** Crea en la tabla `Medidas` (clic derecho ▸ Nueva medida):", ""] + g.bloque_medidas(nuevas)
    elif med:
        L += [f"**Fórmula.** Usa la medida `[{med['nombre']}]`, que ya creaste en {g.medidas_creadas.get(med['codigo'], 'un elemento anterior')}.", ""]
    L += ["**Cómo armarlo en Power BI.**", "",
          "1. En Visualizaciones elige **Tarjeta** y colócala en la fila superior de la página (mira su lugar en el HTML de referencia).",
          f"2. Arrastra la medida `[{med['nombre'] if med else k}]` al campo **Campos**.",
          "3. En Formato ▸ Etiqueta de datos ▸ **Color ▸ Formato condicional ▸ Reglas**: " + (
              f"verde si el valor es {'mayor o igual' if m['cmp'] == '>=' else 'menor o igual'} a {m['meta']:g} y rojo en caso contrario." if m["meta"] is not None else
              "deja un color neutro: este indicador no tiene meta todavía (aparece como «Sin meta»)."),
          f"4. Agrega como subtítulo el texto «Meta: {m['meta_texto']}» y el nombre del indicador como título.", ""]
    esp = f"último mes ({etiqueta_mes(val['mes'])}): **{fmt(val['valor'], val['unidad'])}** → {val['estado']} (meta {m['meta_texto']})."
    meses, vals = kpi_serie(g.resp, k) if k != "KPI-07" else ([], [])
    if vals:
        esp += f" Primer mes ({etiqueta_mes(meses[0])}): {fmt(vals[0], val['unidad'])}."
    L += [f"**Valor esperado.** {esp}"]
    if k == "KPI-05":
        L += ["", "> El pronóstico de referencia usa un método simple: el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. "
              "El pronóstico de Power BI (Analytics ▸ Pronóstico) usa suavizado exponencial con estacionalidad y **no coincidirá exactamente**."]
    L += [""]
    return L


def _visual(g, p, v, n):
    """Elemento de un gráfico, matriz o tabla."""
    g.donde = f"{p['codigo']} · Elemento {n}"
    nuevas = g.medidas_nuevas(v["medidas"])
    usadas = [g.por_codigo[c] for c in v["medidas"] if c in g.por_codigo]
    cols = g.columnas(g.recursivas(v["medidas"]), [v["x"], v.get("serie", "")] + list(v["filtros"]))
    L = [f"### Elemento {n} · {NOMBRE_TIPO[v['tipo']]}: {v['titulo']}", "",
         f"**Qué muestra.** {v['lectura']}", ""]
    expl = [f"- **{m['nombre']}:** {m['explicacion']}" for m in usadas]
    L += ["**Cómo se calcula.**", ""] + (expl or ["- Se arma con los campos de abajo."]) + [""]
    filas = g.tabla_columnas(cols, usadas)
    if filas:
        L += ["**Tablas y columnas.**", ""] + _tabla(["Campo", "Qué es", "De dónde sale"], filas) + [""]
    eje = [["Eje Y (categorías)", v["x"]], ["Eje X (valores)", v["y"]]] if v["tipo"] == "barras" else [["Eje X / filas", v["x"]], ["Valores (eje Y)", v["y"]]]
    if v.get("serie"):
        eje.append(["Leyenda" if v["tipo"] != "matriz" else "Columnas", v["serie"]])
    L += _tabla(["Dónde va", "Campo"], eje) + [""]
    if nuevas:
        L += ["**Fórmulas.** Crea en la tabla `Medidas` las que todavía no tengas:", ""] + g.bloque_medidas(nuevas)
    else:
        L += ["**Fórmulas.** Todas las medidas de este elemento ya las creaste antes: " + ", ".join(f"`[{m['nombre']}]` ({g.medidas_creadas.get(m['codigo'], '')})" for m in usadas) + ".", ""]
    L += ["**Cómo armarlo en Power BI.**", ""] + [f"{i}. {s}" for i, s in enumerate(pasos_visual(v, g.plan), 1)] + [""]
    L += [f"**Valor esperado.** {esperado_resumen(v, g.resp, g.modelo, g.metas)}.", ""]
    if "MED-13" in v["medidas"] or "MED-14" in v["medidas"]:
        L += ["> El pronóstico de referencia es el promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno. "
              "El pronóstico de Power BI **no coincidirá exactamente**; para comparar usa la medida «Pronóstico de referencia».", ""]
    return L


def guia_markdown(plan, resp, modelo, metas, brief):
    g = _Guia(plan, resp, modelo, metas)
    L = ["# Guía paso a paso del dashboard en Power BI", "",
         "Esta guía la ejecuta el equipo en Power BI y está escrita para los datos y el modelo de este proyecto. Hay una sección por página. En cada una vas elemento por elemento "
         "(segmentadores, tarjetas y gráficos) y, en cada elemento, ves qué muestra, cómo se calcula, de qué tablas y columnas sale, su fórmula, cómo armarlo y el valor esperado. "
         "Cada medida y cada columna calculada se explica **en el primer elemento que la usa**; después solo se la menciona. El DAX es una propuesta que se prueba y se ajusta. "
         "Compara cada resultado con el valor esperado y con el HTML `dashboard-referencia.html`.", "",
         f"Antes de la primera página, parte del modelo que dejó el ETL (nueve tablas y nueve relaciones, con `dCalendario` marcada como tabla de fechas) y crea una tabla vacía para guardar las medidas: "
         f"**Inicio ▸ Especificar datos**, con una columna cualquiera, y nómbrala `Medidas`. `fPedidos` conserva todas las filas leídas ({filas_ventas(resp)} en este caso) y las descartadas tienen "
         "`registro_valido` = 0 e importes en 0: por eso las sumas de venta, comisión y costo solo cuentan las filas válidas.", ""]
    for p in plan["paginas"]:
        L += [f"## {p['codigo']} · {p['nombre']}", "", f"**Para quién:** {p['usuario']}. **Pregunta que responde:** {p['pregunta']}", ""]
        n = 1
        seg = p.get("segmentadores", [])
        if seg:
            g.donde = f"{p['codigo']} · Elemento {n}"
            L += [f"### Elemento {n} · Segmentadores", "",
                  "**Qué muestra.** Filtros para recortar toda la página por periodo, canal o turno.", "",
                  "**Tablas y columnas.**", ""] + _tabla(["Campo", "Qué es", "De dónde sale"], g.tabla_columnas([tuple(re.match(r"(\w+)\[(\w+)\]", x).groups()) for x in seg], [])) + [""]
            L += ["**Cómo armarlo en Power BI.**", "",
                  "1. Inserta un **Segmentador** por cada campo de la tabla anterior (arrastra el campo a **Campo**).",
                  "2. Para `dCalendario[nombre_mes]` ordena por `mes`: Herramientas de columna ▸ **Ordenar por columna** ▸ `mes`.",
                  "3. En **Vista ▸ Sincronizar segmentadores** activa la sincronización con las demás páginas.", "",
                  "**Valor esperado.** No tiene valor: al filtrar, todos los elementos de la página deben recalcularse.", ""]
            n += 1
        for k in p.get("kpis", []):
            L += _tarjeta(g, p, k, n)
            n += 1
        for v in p["visuales"]:
            L += _visual(g, p, v, n)
            n += 1
    return "\n".join(L) + "\n"


def texto_paginas(plan):
    out = []
    for p in plan["paginas"]:
        out.append(f"{p['codigo']} · {p['nombre']} ({p['usuario']})\n  Pregunta: {p['pregunta']}\n  KPI: {', '.join(p.get('kpis', []))}\n  Segmentadores: {', '.join(p.get('segmentadores', []))}")
        for v in p["visuales"]:
            out.append(f"  - Visual {v['id']} [{v['tipo']}] {v['titulo']}\n      X: {v['x']}\n      Y: {v['y']}\n      Origen: {', '.join(v['origen'])}")
    return "\n".join(out) + "\n"


def texto_medidas(plan):
    return "\n\n".join(f"{m['codigo']} · {m['nombre']}\n{m['dax']}" for m in plan["medidas"]) + "\n"


# ------------------------------------------------------------------ coherencia y orquestación
def comprobar_plan(plan, modelo, resp):
    """Causas (vacío si está bien) de un plan: tipos, fuentes de datos, KPI, medidas y DAX que cita campos fuera del modelo."""
    causas = []
    kpis = {k["codigo"] for k in modelo.get("kpis", [])}
    medidas = {m["codigo"]: m for m in plan.get("medidas", [])}
    nombres = {m["nombre"] for m in medidas.values()}
    for m in medidas.values():
        causas += [f"{m['codigo']}: {c}" for c in DAX.problemas_dax(m["dax"], modelo, nombres)]
    cubiertos = set()
    for p in plan.get("paginas", []):
        cubiertos |= set(p.get("kpis", []))
        cubiertos |= {medidas[c]["kpi"] for v in p.get("visuales", []) for c in v["medidas"] if c in medidas and medidas[c]["kpi"]}
        for k in p.get("kpis", []):
            if k not in kpis:
                causas.append(f"{p['codigo']}: el KPI {k} no está en el modelo")
        for v in p.get("visuales", []):
            ref = f"{p['codigo']} visual {v['id']}"
            if v["tipo"] not in TIPOS:
                causas.append(f"{ref}: tipo desconocido {v['tipo']}")
            if v["datos"]["fuente"] not in FUENTES:
                causas.append(f"{ref}: fuente de datos desconocida {v['datos']['fuente']}")
            causas += [f"{ref}: la medida {c} no está definida" for c in v["medidas"] if c not in medidas]
    causas += [f"el KPI {k} no está en ninguna página" for k in sorted(kpis - cubiertos)]
    return causas


def construir(raiz, run):
    run = Path(run)
    plan = cargar_plan(run)
    resp = cargar_respuestas(raiz)
    modelo = cargar_modelo(raiz)
    causas = comprobar_plan(plan, modelo, resp)
    if causas:
        raise ErrorReferencia("el plan no es coherente: " + "; ".join(causas))
    metas = metas_kpi(modelo)
    import brief as BR
    try:
        brief = BR.vigente(raiz)
    except Exception:
        brief = {}
    tokens = H.tokens_del_proyecto(raiz)
    mat = run / "materiales"
    mat.mkdir(parents=True, exist_ok=True)
    (mat / "dashboard-referencia.html").write_text(html_referencia(plan, resp, modelo, metas, brief, tokens), encoding="utf-8")
    (mat / "guia-dashboard.md").write_text(guia_markdown(plan, resp, modelo, metas, brief), encoding="utf-8")
    (mat / "paginas.txt").write_text(texto_paginas(plan), encoding="utf-8")
    (mat / "medidas.txt").write_text(texto_medidas(plan), encoding="utf-8")
    return mat


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("plan", "construir"):
        s = sub.add_parser(n)
        s.add_argument("--run", required=True)
        s.add_argument("--raiz", default=".")
    a = ap.parse_args(argv)
    try:
        run = Path(a.run) if Path(a.run).is_absolute() or Path(a.run).exists() else Path(a.raiz) / "project" / "09-dashboard" / a.run
        if a.cmd == "plan":
            destino = run / "materiales" / "paginas.json"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(PLAN_POR_DEFECTO.read_text(encoding="utf-8"), encoding="utf-8")
            print(destino)
            return 0
        print(construir(a.raiz, run))
        return 0
    except ErrorReferencia as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
