#!/usr/bin/env python3
"""Genera data/limpio/: un CSV por tabla del modelo en estrella (9 tablas), listos para importar en Power BI sin pasos manuales.

  python3 scripts/generar_limpio_modelo.py [--raiz .]

Parte de la limpieza de .claude/skills/_shared/etl_limpio.py (se ejecuta sobre una copia temporal para no mezclar sus archivos)
y construye las columnas del modelo (claves, medidas, banderas de calidad, metas). Los nombres de tabla y de columna son los del
diagrama del modelo. No se descarta ninguna fila de pedidos: los duplicados y los inválidos quedan con registro_valido = 0 y sus
medidas en 0, de modo que registro_total cuenta todo y KPI-01 se calcula directo.
"""
import argparse
import csv
import datetime as dt
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / ".claude" / "skills" / "_shared"))
import etl_limpio as EL  # noqa: E402
import etl_referencia as ER  # noqa: E402

FERIADOS = {101, 501, 629, 728, 729, 830, 1008, 1101, 1208, 1225}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
ABR = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
CANALES = [(1, "Salón", "Propio", 0), (2, "Para llevar", "Propio", 0), (3, "WhatsApp", "Propio", 0),
           (4, "Rappi", "Aplicación", 30), (5, "PedidosYa", "Aplicación", 25)]
TURNOS = [(1, "Mañana", "11:00", "15:00"), (2, "Tarde", "15:00", "19:00"), (3, "Noche", "19:00", "23:00")]
# KPI de modelo.json (2.5): código, nombre, objetivo, meta numérica (None = Pendiente), frecuencia
KPIS = [(1, "Calidad de datos del ETL", "OE-01", 98, "Por carga"),
        (2, "Margen de contribución por canal y producto", "OE-02", None, "Mensual"),
        (3, "Margen neto global", "OE-02", 12, "Mensual"),
        (4, "Porcentaje de merma por turno", "OE-03", 3, "Diaria"),
        (5, "Precisión del pronóstico de demanda", "OE-03", 15, "Semanal"),
        (6, "Precio promedio del pollo vivo por kilogramo", "OE-04", None, "Semanal"),
        (7, "KPI con meta en el dashboard", "OE-05", 100, "Por carga")]


LEEME = """# data/limpio: una tabla del modelo por CSV

Importa cada CSV en Power BI con el nombre del archivo como nombre de tabla (Obtener datos > Texto/CSV). Ya están todas las columnas del diagrama; no hay que crear columnas ni limpiar nada.

| Archivo | Filas | Clave |
|---|---|---|
| fPedidos | {fPedidos} | fecha_key, producto_key, canal_key, turno_key |
| fProduccion | {fProduccion} | fecha_key, turno_key |
| fPrecioInsumo | {fPrecioInsumo} | fecha_key |
| fMetaKpi | {fMetaKpi} (7 KPI x 15 meses) | kpi_key, fecha_key |
| dCalendario | {dCalendario} | fecha_key |
| dProducto / dCanal / dTurno / dKpi | {dProducto} / {dCanal} / {dTurno} / {dKpi} | producto_key / canal_key / turno_key / kpi_key |

- fPedidos conserva TODAS las filas. Duplicados e inválidos tienen registro_valido = 0 y sus medidas en 0; registro_total = 1 en todas.
- fProduccion excluye las jornadas repetidas o con vendidos > preparados, según las reglas del ETL.
- Tipos en Power BI: *_key, cantidad, registro_*, pollos_* y valor_imputado = entero; venta_bruta, comision, costo_*, pollos_equivalentes, precio_kg, meta, valor_real = decimal; es_feriado y tiene_meta = verdadero/falso; fecha = fecha.
- dCalendario trae tres columnas extra que usa el dashboard: num_dia_semana (ordena dia_semana), anio_mes (ordena mes_anio) y mes_anio (texto «ago 25», eje X de los gráficos mensuales). Ordena nombre_mes por la columna mes.
- fMetaKpi: meta vacía en KPI-02 y KPI-06 (Pendiente). valor_real viene de data/respuestas/kpi-esperados.csv; KPI-07 queda vacío (lo calcula el DAX).
- Regenerar: python3 scripts/generar_limpio_modelo.py
"""


def leer(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def escribir(p, cols, filas):
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows([[fila[c] for c in cols] for fila in filas])
    return len(filas)


def fkey(d):
    return d.year * 10000 + d.month * 100 + d.day


def r2(x):
    return f"{x:.2f}"


def construir(raiz):
    raiz = Path(raiz)
    out = raiz / "data" / "limpio"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:  # limpieza intermedia sin ensuciar data/limpio
        (Path(tmp) / "data").mkdir()
        for f in (raiz / "data").glob("*.csv"):
            shutil.copy(f, Path(tmp) / "data" / f.name)
        EL.limpiar(tmp)
        inter = Path(tmp) / "data" / "limpio"
        pedidos, prod = leer(inter / "pedidos.csv"), leer(inter / "produccion.csv")
        precios, catalogo, costos = leer(inter / "precios-pollo.csv"), leer(inter / "catalogo-productos.csv"), leer(inter / "costos-operativos.csv")

    cat = {c["producto"]: c for c in catalogo}
    prod_key = {c["producto"]: i for i, c in enumerate(catalogo, 1)}
    canal_key = {n: k for k, n, _, _ in CANALES}
    turno_key = {n: k for k, n, _, _ in TURNOS}
    precio = {r["fecha"]: float(r["precio_kg"]) for r in precios}
    costo_mes = {c["mes"]: float(c["total"]) for c in costos}

    # ---- fPedidos
    filas = []
    for p in pedidos:
        valido = int(p["es_duplicado"] == "0" and p["es_invalido"] == "0")
        cant = float(p["cantidad"] or 0)
        fecha = p["fecha"]
        venta = com = costo = peq = 0.0
        if valido:
            if p["fuente"] == "FUE-01":
                venta = cant * float(p["precio_unitario"]) - float(p["descuento"] or 0)
            else:
                venta = float(p["monto_origen"])
            if p["canal"] == "Rappi":
                com = float(p["comision_origen"])
            elif p["canal"] == "PedidosYa":
                com = venta * float(p["comision_pct"]) / 100
            c = cat[p["producto"]]
            costo = cant * (float(c["kg_pollo_vivo"]) * precio[fecha] + float(c["costo_otros"]))
            peq = cant * float(c["pollos_equivalentes"])
        filas.append({"fecha_key": fkey(dt.date.fromisoformat(fecha)), "producto_key": prod_key[p["producto"]],
                      "canal_key": canal_key[p["canal"]], "turno_key": turno_key[p["turno"]], "cantidad": int(cant),
                      "venta_bruta": venta, "comision": com, "costo_estimado": costo, "costo_operativo": 0.0,
                      "pollos_equivalentes": peq, "registro_valido": valido, "registro_total": 1, "_mes": fecha[:7]})
    venta_mes = defaultdict(float)
    for f in filas:
        venta_mes[f["_mes"]] += f["venta_bruta"]
    for f in filas:  # costo operativo del mes repartido en proporción a la venta
        f["costo_operativo"] = costo_mes[f["_mes"]] * f["venta_bruta"] / venta_mes[f["_mes"]]
    for f in filas:
        for c in ("venta_bruta", "comision", "costo_estimado", "costo_operativo", "pollos_equivalentes"):
            f[c] = r2(f[c])
    cols = ["fecha_key", "producto_key", "canal_key", "turno_key", "cantidad", "venta_bruta", "comision", "costo_estimado",
            "costo_operativo", "pollos_equivalentes", "registro_valido", "registro_total"]
    n = {"fPedidos": escribir(out / "fPedidos.csv", cols, filas)}

    # ---- fProduccion
    n["fProduccion"] = escribir(out / "fProduccion.csv", ["fecha_key", "turno_key", "pollos_preparados", "pollos_vendidos", "pollos_merma"],
                                [{"fecha_key": fkey(dt.date.fromisoformat(p["fecha"])), "turno_key": turno_key[p["turno"]],
                                  "pollos_preparados": p["pollos_preparados"], "pollos_vendidos": p["pollos_vendidos"],
                                  "pollos_merma": p["pollos_merma"]} for p in prod])

    # ---- fPrecioInsumo
    n["fPrecioInsumo"] = escribir(out / "fPrecioInsumo.csv", ["fecha_key", "precio_kg", "valor_imputado"],
                                  [{"fecha_key": fkey(dt.date.fromisoformat(r["fecha"])), "precio_kg": r["precio_kg"],
                                    "valor_imputado": r["valor_imputado"]} for r in precios])

    # ---- dCalendario (periodo completo de los datos)
    d0, d1 = dt.date.fromisoformat(precios[0]["fecha"]), dt.date.fromisoformat(precios[-1]["fecha"])
    cal, d = [], d0
    while d <= d1:
        cal.append({"fecha_key": fkey(d), "fecha": d.isoformat(), "anio": d.year, "mes": d.month, "nombre_mes": MESES[d.month - 1],
                    "dia_semana": DIAS[d.weekday()], "es_feriado": "TRUE" if d.month * 100 + d.day in FERIADOS else "FALSE",
                    "num_dia_semana": d.weekday() + 1, "anio_mes": d.year * 100 + d.month,
                    "mes_anio": f"{ABR[d.month - 1]} {d.year % 100}"})
        d += dt.timedelta(days=1)
    n["dCalendario"] = escribir(out / "dCalendario.csv", list(cal[0]), cal)

    # ---- dimensiones pequeñas
    n["dProducto"] = escribir(out / "dProducto.csv", ["producto_key", "producto", "categoria"],
                              [{"producto_key": i, "producto": c["producto"], "categoria": c["categoria"]} for i, c in enumerate(catalogo, 1)])
    n["dCanal"] = escribir(out / "dCanal.csv", ["canal_key", "canal", "tipo_canal", "comision_pct"],
                           [{"canal_key": k, "canal": c, "tipo_canal": t, "comision_pct": p} for k, c, t, p in CANALES])
    n["dTurno"] = escribir(out / "dTurno.csv", ["turno_key", "turno", "hora_inicio", "hora_fin"],
                           [{"turno_key": k, "turno": t, "hora_inicio": a, "hora_fin": b} for k, t, a, b in TURNOS])
    n["dKpi"] = escribir(out / "dKpi.csv", ["kpi_key", "kpi", "objetivo", "tiene_meta", "frecuencia"],
                         [{"kpi_key": k, "kpi": nom, "objetivo": ob, "tiene_meta": "TRUE" if m is not None else "FALSE", "frecuencia": fr}
                          for k, nom, ob, m, fr in KPIS])

    # ---- fMetaKpi: una fila por KPI y mes; valor_real de la hoja de respuestas (KPI-07 sin valor, lo calcula el DAX)
    esperado = {(r["kpi"], r["mes"]): r["valor"] for r in leer(raiz / "data" / "respuestas" / "kpi-esperados.csv")}
    meses = sorted({c["fecha_key"] // 100 for c in cal})
    meta = []
    for k, _, _, m, _ in KPIS:
        for ym in meses:
            mes = f"{ym // 100}-{ym % 100:02d}"
            meta.append({"kpi_key": k, "fecha_key": ym * 100 + 1, "meta": "" if m is None else m,
                         "valor_real": esperado.get((f"KPI-{k:02d}", mes), "")})
    n["fMetaKpi"] = escribir(out / "fMetaKpi.csv", ["kpi_key", "fecha_key", "meta", "valor_real"], meta)
    (out / "LEEME.md").write_text(LEEME.format(**n), encoding="utf-8")
    return out, n, filas


def verificar(raiz, filas):
    """Compara con data/respuestas/: venta y comisión por mes y canal."""
    esp = {(r["mes"], r["canal"]): (float(r["ventas"]), float(r["comision"])) for r in leer(Path(raiz) / "data" / "respuestas" / "ventas-mes-canal.csv")}
    canal = {k: n for k, n, _, _ in CANALES}
    got = defaultdict(lambda: [0.0, 0.0])
    for f in filas:
        g = got[(f["_mes"], canal[f["canal_key"]])]
        g[0] += float(f["venta_bruta"])
        g[1] += float(f["comision"])
    mal = [(k, esp[k], got[k]) for k in esp if abs(esp[k][0] - got[k][0]) > 1 or abs(esp[k][1] - got[k][1]) > 1]
    return len(esp), mal


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=".")
    raiz = ap.parse_args(argv).raiz
    out, n, filas = construir(raiz)
    total, mal = verificar(raiz, filas)
    for k, v in n.items():
        print(f"{k:14} {v:>7} filas")
    print(f"Verificación venta/comisión por mes y canal: {total - len(mal)}/{total} coinciden con data/respuestas/")
    for m in mal[:10]:
        print("  diferencia:", m)
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
