#!/usr/bin/env python3
"""Genera ds-final.html: el dashboard de referencia reducido a 2 páginas con los KPI y gráficos más importantes.

  python3 scripts/generar_ds_final.py [--run project/09-dashboard/<corrida>] [--raiz .]

Toma los visuales ya definidos en materiales/paginas.json (mismos datos, mismas medidas y las mismas cajas «Cómo construirlo en
Power BI») y los reordena en dos páginas. Escribe materiales/ds-final.html junto al dashboard-referencia.html.
"""
import argparse
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".claude" / "skills" / "_shared"))
import brief as BR  # noqa: E402
import dashboard_ref as R  # noqa: E402
import html_tpl as H  # noqa: E402

# (página original, id del visual, posición nueva [columna, fila, ancho, alto])
PAGINAS = [
    {"codigo": "PAG-01", "nombre": "Resumen del negocio", "usuario": "Dueño",
     "pregunta": "¿Gana el negocio lo que debería y dónde se pierde: en margen o en merma?",
     "kpis": ["KPI-03", "KPI-01", "KPI-04"], "segmentadores": ["dCalendario[anio]", "dCalendario[nombre_mes]", "dCanal[canal]"],
     "visuales": [("PAG-01", 1, [1, 1, 6, 1]), ("PAG-03", 1, [7, 1, 6, 1]), ("PAG-01", 3, [1, 2, 12, 1])]},
    {"codigo": "PAG-02", "nombre": "Rentabilidad por canal", "usuario": "Dueño",
     "pregunta": "¿Qué canales dejan margen después de la comisión y cuánto pesa cada uno en la venta?",
     "kpis": ["KPI-02"], "segmentadores": ["dCalendario[anio]", "dCalendario[nombre_mes]", "dProducto[categoria]"],
     "visuales": [("PAG-02", 1, [1, 1, 5, 1]), ("PAG-02", 4, [6, 1, 7, 1]), ("PAG-02", 3, [1, 2, 12, 1])]},
]


def seccion_medidas(plan, paginas):
    """Sección «Medidas DAX globales»: todas las medidas que usa ds-final, en el orden en que hay que crearlas."""
    g = R._Guia(plan, {}, {}, {})
    usos = {}  # código de medida -> lugares donde se usa

    def anotar(codigos, lugar):
        for c in g.recursivas(codigos):
            usos.setdefault(c["codigo"], [])
            if lugar not in usos[c["codigo"]]:
                usos[c["codigo"]].append(lugar)
    pedidas = []
    for p in paginas:
        for k in p.get("kpis", []):
            med = R._medida_de_kpi(plan, k)
            if med:
                pedidas.append(med["codigo"])
                anotar([med["codigo"]], f"{p['codigo']} · tarjeta {k}")
        for v in p["visuales"]:
            pedidas += v["medidas"]
            anotar(v["medidas"], f"{p['codigo']} · gráfico {v['id']}")
    orden = g.medidas_nuevas(list(dict.fromkeys(pedidas)))
    filas = []
    for n, m in enumerate(orden, 1):
        cols = ", ".join(f"{t}[{c}]" for t, c in g.columnas([m]))
        previas = [x for x in dict.fromkeys(R.RE_MEDIDA.findall(m["dax"])) if x in g.por_nombre and x != m["nombre"]]
        lugares = "; ".join(usos.get(m["codigo"], []))
        filas.append(
            f'<div class="caja"><h4><span class="num">{n}</span> [{R.esc(m["nombre"])}]</h4><p class="cm">{R.esc(m["codigo"])} · medida DAX</p>'
            f'<p class="fmt" style="margin:0 0 6px">{R.esc(m["explicacion"])}</p>'
            f'<div class="med"><code>{R.esc(m["nombre"])} =\n{R.esc(m["dax"])}</code>'
            f'<span>Columnas que usa: {R.esc(cols) if cols else "ninguna directa"}.'
            f'{" Necesita antes: " + R.esc(", ".join("[" + x + "]" for x in previas)) + "." if previas else ""}</span></div>'
            f'<p class="fmt">Se usa en: {R.esc(lugares)}.</p></div>')
    return ('<section class="final" id="medidas"><h2>Medidas DAX globales</h2><p class="preg">Créalas una sola vez, en este orden, y después úsalas en todas las páginas. '
            'Primero crea la tabla que las guarda: Inicio ▸ Especificar datos, con una columna cualquiera, y nómbrala <b>Medidas</b>. '
            'Luego, con esa tabla seleccionada, usa Nueva medida para cada una. Cada medida solo depende de las anteriores de la lista. '
            'Los nombres deben quedar exactamente como se ven, porque las otras fórmulas los llaman entre corchetes.</p>'
            f'<div class="cajas">{"".join(filas)}</div></section>')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default="project/09-dashboard/22-11-2026-18-39-12")
    ap.add_argument("--raiz", default=".")
    a = ap.parse_args(argv)
    run = Path(a.run)
    plan = R.cargar_plan(run)
    orig = {(p["codigo"], v["id"]): v for p in plan["paginas"] for v in p["visuales"]}
    nuevo = copy.deepcopy(plan)
    nuevo["paginas"] = []
    for p in PAGINAS:
        vis = []
        for n, (pg, vid, pos) in enumerate(p["visuales"], 1):
            v = copy.deepcopy(orig[(pg, vid)])
            v["id"], v["pos"] = n, pos
            vis.append(v)
        nuevo["paginas"].append({**{k: p[k] for k in ("codigo", "nombre", "usuario", "pregunta", "kpis", "segmentadores")}, "visuales": vis})
    resp, modelo = R.cargar_respuestas(a.raiz), R.cargar_modelo(a.raiz)
    metas = R.metas_kpi(modelo)
    try:
        brief = BR.vigente(a.raiz)
    except Exception:
        brief = {}
    html = R.html_referencia(nuevo, resp, modelo, metas, brief, H.tokens_del_proyecto(a.raiz))
    html = html.replace('<section class="final" id="medidas-tarjetas">', seccion_medidas(nuevo, nuevo["paginas"]) + '<section class="final" id="medidas-tarjetas">', 1)
    html = (html.replace("Dashboard de referencia", "Dashboard final")
                .replace("Así debería verse y estos son los valores esperados. Se construye en Power BI.", "Versión final de 2 páginas con los KPI y gráficos más importantes. Se construye en Power BI."))
    destino = run / "materiales" / "ds-final.html"
    destino.write_text(html, encoding="utf-8")
    print(destino)


if __name__ == "__main__":
    main()
