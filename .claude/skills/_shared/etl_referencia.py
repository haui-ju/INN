#!/usr/bin/env python3
"""Limpieza de referencia del ETL: sigue los mismos pasos que la guía de Power Query y devuelve los puntos de control.

  python3 .claude/skills/_shared/etl_referencia.py [--raiz .]      (imprime en JSON los puntos de control de data/)

Sirve para dos cosas: dar a la guía del equipo las filas que deben quedar después de cada paso, y comprobar que esas cifras
coinciden con la hoja de respuestas (data/respuestas/). Es la forma «correcta» de limpiar; el equipo la repite en Power Query.
Convenciones: las copias duplicadas se cuentan solo como duplicados (los demás defectos se cuentan sobre los registros únicos);
los pedidos duplicados e inválidos se conservan en fPedidos con registro_valido = 0 y sus medidas en 0. Solo biblioteca estándar.
"""
import argparse
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

HORAS = {11: "Mañana", 12: "Mañana", 13: "Mañana", 14: "Mañana", 15: "Tarde", 16: "Tarde", 17: "Tarde", 18: "Tarde",
         19: "Noche", 20: "Noche", 21: "Noche", 22: "Noche"}
CANAL_DE = {"fue-02": "Rappi", "fue-03": "PedidosYa", "fue-04": "WhatsApp"}


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fecha_texto(t):
    """Fecha de un texto en AAAA-MM-DD o DD/MM/AAAA, con hora opcional; None si está vacío o no se entiende."""
    s = (t or "").strip()[:10]
    if not s:
        return None
    try:
        return dt.datetime.strptime(s, "%d/%m/%Y").date() if "/" in s else dt.date.fromisoformat(s)
    except ValueError:
        return None


def hora_de(t):
    """Hora (entero) de «AAAA-MM-DD HH:MM[:SS]» o de «HH:MM»; None si no hay."""
    s = (t or "").strip()
    s = s.split(" ")[-1] if " " in s else s
    return int(s[:2]) if len(s) >= 4 and s[2] == ":" and s[:2].isdigit() else None


def numero(t):
    s = (t or "").strip()
    try:
        return float(s) if s != "" else None
    except ValueError:
        return None


def unicas(filas):
    """(filas sin las copias exactas, número de copias): se conserva la primera aparición."""
    vistas, out = set(), []
    for f in filas:
        k = tuple(f.values())
        if k not in vistas:
            vistas.add(k)
            out.append(f)
    return out, len(filas) - len(out)


def _alias(catalogo):
    m = {}
    for c in catalogo:
        m[c["producto"]] = c["producto"]
        for a in c["alias"].split("|"):
            m[a] = c["producto"]
    return m


def _lineas(data, canon=(), dedupe=True):
    """Líneas de las cuatro fuentes de ventas en el esquema común, tras quitar las copias exactas de cada archivo."""
    out, cont = [], {}
    cuentas = {}
    for fu, archivo in (("fue-01", "fue-01-caja.csv"), ("fue-02", "fue-02-rappi.csv"), ("fue-03", "fue-03-pedidosya.csv"), ("fue-04", "fue-04-whatsapp.csv")):
        brutas = leer(data / archivo)
        unic, dup = unicas(brutas)
        if not dedupe:
            unic = brutas
        col_fecha = {"fue-01": "fecha", "fue-02": "fecha_hora", "fue-03": "fecha", "fue-04": "fecha"}[fu]
        barras = (lambda f: "-" in f[col_fecha].split(" ")[0]) if fu == "fue-03" else (lambda f: "/" in f[col_fecha])
        col_prod = {"fue-01": "producto", "fue-02": "producto", "fue-03": "item", "fue-04": "producto"}[fu]
        c = {"filas": len(brutas), "duplicados": dup, "tras_duplicados": len(unic), "formato_fecha": 0, "nulo": 0, "invalidos": 0,
             # lo que se ve en el archivo tal cual llega, con las copias duplicadas incluidas
             "formato_fecha_archivo": sum(barras(f) for f in brutas),
             "nombre_producto_archivo": sum(f[col_prod] not in canon for f in brutas) if canon else 0,
             "nulo_archivo": sum((f.get("turno") == "") + (f.get("descuento") == "") for f in brutas),
             "cancelados": sum(f.get("estado") == "CANCELADO" for f in unic),
             "monto_cancelados": round(sum(numero(f.get("monto") or f.get("total")) or 0 for f in unic if f.get("estado") == "CANCELADO"), 2)}
        for f in unic:
            if fu == "fue-01":
                fe, cant, precio = fecha_texto(f["fecha"]), numero(f["cantidad"]), numero(f["precio_unitario"])
                hora, canal, prod = hora_de(f["hora"]), f["canal"], f["producto"]
                desc = numero(f["descuento"])
                c["formato_fecha"] += "/" in f["fecha"]
                c["nulo"] += (f["turno"] == "") + (f["descuento"] == "")
                invalido = cant is None or cant <= 0 or precio is None
                monto = None if invalido else round(cant * precio - (desc or 0), 2)
                comision = 0.0
                ped = f["ticket_id"]
            elif fu == "fue-02":
                fe, cant, monto = fecha_texto(f["fecha_hora"]), numero(f["cantidad"]), numero(f["monto"])
                hora, canal, prod, ped = hora_de(f["fecha_hora"]), "Rappi", f["producto"], f["pedido_id"]
                c["formato_fecha"] += "/" in f["fecha_hora"]
                invalido = monto is None or f["estado"] == "CANCELADO"
                comision = numero(f["comision"]) or 0.0
            elif fu == "fue-03":
                fe, cant, monto = fecha_texto(f["fecha"]), numero(f["cant"]), numero(f["total"])
                hora, canal, prod, ped = hora_de(f["fecha"]), "PedidosYa", f["item"], f["nro_pedido"]
                c["formato_fecha"] += "-" in f["fecha"].split(" ")[0]
                invalido = monto is None or f["estado"] == "CANCELADO"
                comision = round(monto * int(f["comision_pct"]) / 100, 2) if monto is not None else 0.0
            else:
                fe, cant, monto = fecha_texto(f["fecha"]), numero(f["cantidad"]), numero(f["monto"])
                hora, canal, prod, ped = hora_de(f["fecha"]), "WhatsApp", f["producto"], f["pedido"]
                c["formato_fecha"] += "/" in f["fecha"]
                invalido = cant is None or cant <= 0 or monto is None
                comision = 0.0
            c["invalidos"] += invalido
            out.append({"fu": fu, "ped": ped, "fecha": fe, "hora": hora, "canal": canal, "prod_fuente": prod, "cant": cant or 0,
                        "monto": 0.0 if invalido else monto, "comision": 0.0 if invalido else comision, "valido": not invalido,
                        "tel": f.get("telefono")})
        c["validas"] = c["tras_duplicados"] - c["invalidos"]
        cuentas[fu] = c
    return out, cuentas


def puntos_de_control(raiz="."):
    data = Path(raiz) / "data"
    catalogo = leer(data / "apoyo-catalogo-productos.csv")
    cat = {c["producto"]: c for c in catalogo}
    alias = _alias(catalogo)
    lineas, fuentes = _lineas(data, set(cat))
    sin_dedupe, _ = _lineas(data, set(cat), dedupe=False)
    nombres_distintos = defaultdict(int)
    for l in lineas:
        l["producto"] = alias.get(l["prod_fuente"])
        if l["producto"] != l["prod_fuente"]:
            nombres_distintos[l["fu"]] += 1
    for fu, c in fuentes.items():
        c["nombre_producto"] = nombres_distintos[fu]
    # precio diario con el último precio disponible
    precios = {}
    for f in leer(data / "fue-06-precios-pollo.csv"):
        precios[fecha_texto(f["fecha"])] = float(f["precio_kg"])
    a, b = min(precios), max(precios)
    efectivo, imputados, ultimo, d = {}, [], None, a
    while d <= b:
        if d in precios:
            ultimo = precios[d]
        else:
            imputados.append(d)
        efectivo[d] = ultimo
        d += dt.timedelta(days=1)
    # costos operativos mensuales y medidas por línea
    ops = {o["mes"]: float(o["total"]) for o in leer(data / "apoyo-costos-operativos.csv")}
    venta_mes = defaultdict(float)
    for l in lineas:
        l["mes"] = l["fecha"].strftime("%Y-%m")
        k = cat[l["producto"]]
        l["costo"] = round(l["cant"] * (float(k["kg_pollo_vivo"]) * efectivo[l["fecha"]] + float(k["costo_otros"])), 4) if l["valido"] else 0.0
        l["pe"] = l["cant"] * float(k["pollos_equivalentes"]) if l["valido"] else 0.0
        venta_mes[l["mes"]] += l["monto"]
    # tras quitar las copias exactas no debe quedar ninguna clave (pedido, producto) repetida: así la clave sirve para detectar duplicados
    vistos, colisiones = set(), 0
    for l in lineas:
        k = (l["ped"], l["producto"])
        colisiones += k in vistos
        vistos.add(k)
    pedidos = len(lineas)
    pedidos_validos = sum(l["valido"] for l in lineas)
    ventas = defaultdict(lambda: [0, 0.0, 0.0, 0.0])
    for l in lineas:
        if l["valido"]:
            x = ventas[(l["mes"], l["canal"])]
            x[0] += 1
            x[1] += l["monto"]
            x[2] += l["comision"]
            x[3] += l["costo"]
    por_mes = defaultdict(lambda: [0.0, 0.0, 0.0])
    for (m, c), x in ventas.items():
        por_mes[m][0] += x[1]
        por_mes[m][1] += x[2]
        por_mes[m][2] += x[3]
    # producción
    prod_bruta = leer(data / "fue-05-produccion.csv")
    prod_unica, prod_dup = unicas(prod_bruta)
    prod_inval = sum(1 for f in prod_unica if numero(f["pollos_vendidos"]) is None or numero(f["pollos_preparados"]) is None
                     or numero(f["pollos_vendidos"]) > numero(f["pollos_preparados"]))
    prod = {"filas": len(prod_bruta), "duplicados": prod_dup, "tras_duplicados": len(prod_unica), "invalidos": prod_inval,
            "validas": len(prod_unica) - prod_inval, "formato_fecha": sum("/" in f["fecha"] for f in prod_unica),
            "nulo": sum(f["responsable"] == "" for f in prod_unica)}
    fechas_prod = {fecha_texto(f["fecha"]) for f in prod_unica}
    telefonos = {l["tel"] for l in lineas if l["tel"]}
    dias = (b - a).days + 1
    return {
        "periodo": {"inicio": a.isoformat(), "fin": b.isoformat(), "dias": dias},
        "fuentes": {**fuentes, "fue-05": prod,
                    "fue-06": {"filas": len(precios), "dias_sin_precio": len(imputados), "formato_fecha": sum("/" in f["fecha"] for f in leer(data / "fue-06-precios-pollo.csv")),
                               "tras_duplicados": len(precios), "validas": len(precios)}},
        "pedidos": {"filas": sum(fuentes[f]["filas"] for f in fuentes), "duplicados": sum(fuentes[f]["duplicados"] for f in fuentes),
                    "colisiones_de_clave": colisiones,
                    "tras_duplicados": sum(fuentes[f]["tras_duplicados"] for f in fuentes), "invalidos": sum(fuentes[f]["invalidos"] for f in fuentes),
                    "validas": pedidos_validos, "sin_homologar": sum(1 for l in lineas if l["producto"] is None),
                    "turno_derivable": sum(1 for l in lineas if l["hora"] in HORAS)},
        "tablas": {"fPedidos": sum(fuentes[f]["filas"] for f in fuentes), "fProduccion": prod["validas"], "fPrecioInsumo": dias, "fMetaKpi": 7 * len(por_mes),
                   "dCalendario": dias, "dProducto": len(catalogo), "dCanal": 5, "dTurno": 3, "dKpi": 7},
        "precio": {"filas": len(precios), "dias": dias, "imputados": len(imputados), "precio_1_julio": efectivo.get(dt.date(2026, 7, 1)),
                   "precio_14_julio": efectivo.get(dt.date(2026, 7, 14))},
        "telefonos_distintos": len(telefonos),
        "totales": {"ventas": round(sum(v[0] for v in por_mes.values()), 2), "comision": round(sum(v[1] for v in por_mes.values()), 2),
                    "costo_estimado": round(sum(v[2] for v in por_mes.values()), 2), "costo_operativo": round(sum(ops.values()), 2),
                    "lineas": pedidos_validos},
        "meses": {m: {"ventas": round(v[0], 2), "comision": round(v[1], 2), "costo_estimado": round(v[2], 2), "costo_operativo": ops[m]} for m, v in sorted(por_mes.items())},
        "canales": {c: {"lineas": sum(x[0] for (m, cc), x in ventas.items() if cc == c), "ventas": round(sum(x[1] for (m, cc), x in ventas.items() if cc == c), 2),
                        "comision": round(sum(x[2] for (m, cc), x in ventas.items() if cc == c), 2)} for c in ("Salón", "Para llevar", "WhatsApp", "Rappi", "PedidosYa")},
        "ventas_mes_canal": {f"{m}|{c}": [x[0], round(x[1], 2), round(x[2], 2)] for (m, c), x in sorted(ventas.items())},
        "jornadas_produccion": len(fechas_prod),
        # cuánto se desvían las ventas si un defecto no se trata
        "efecto_ventas": {"duplicados": round(sum(l["monto"] for l in sin_dedupe) - sum(l["monto"] for l in lineas), 2),
                          "cancelados": round(sum(fuentes[f]["monto_cancelados"] for f in fuentes), 2)},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=".")
    a = ap.parse_args(argv)
    print(json.dumps(puntos_de_control(a.raiz), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
