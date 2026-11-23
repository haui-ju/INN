#!/usr/bin/env python3
"""Datos limpios: aplica la limpieza y la estandarización del ETL a los CSV de data/ y deja el resultado en data/limpio/.

  python3 .claude/skills/_shared/etl_limpio.py [--raiz .]

Deja SIN crear las columnas del modelo (claves, venta_bruta, comision, costo_estimado, costo_operativo, pollos_equivalentes,
registro_valido, registro_total, metas): esas las construye el equipo en Power BI. Lo que sí hace es lo que la guía llama limpieza:
fechas en AAAA-MM-DD, producto homologado con el catálogo, turno completo, descuento vacío en 0, teléfono reemplazado por un código,
copias duplicadas e inválidas marcadas (no borradas) en pedidos, jornadas duplicadas o inválidas fuera de producción y días sin precio
completados con el último precio publicado. Reutiliza etl_referencia.py, de modo que las cifras coinciden con data/respuestas/.
"""
import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import etl_referencia as ER  # noqa: E402

PEDIDOS = ["pedido_id", "fuente", "fecha", "hora", "turno", "canal", "producto", "cantidad", "precio_unitario", "descuento",
           "monto", "comision", "comision_pct", "estado", "cliente_id", "es_duplicado", "es_invalido"]


def _escribir(ruta, cols, filas):
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)


def _num(x):
    return "" if x is None else (str(int(x)) if float(x) == int(x) else f"{x:.2f}")


def _hhmm(h):
    return "" if h is None else f"{h:02d}:00"


def limpiar(raiz="."):
    raiz = Path(raiz)
    data, out = raiz / "data", raiz / "data" / "limpio"
    out.mkdir(exist_ok=True)
    catalogo = ER.leer(data / "apoyo-catalogo-productos.csv")
    alias = ER._alias(catalogo)
    clientes = {}
    pedidos = []
    cfg = {  # fuente: (archivo, canal fijo, columnas de pedido, fecha, producto, cantidad, monto)
        "FUE-01": ("fue-01-caja.csv", None, "ticket_id", "fecha", "producto", "cantidad"),
        "FUE-02": ("fue-02-rappi.csv", "Rappi", "pedido_id", "fecha_hora", "producto", "cantidad"),
        "FUE-03": ("fue-03-pedidosya.csv", "PedidosYa", "nro_pedido", "fecha", "item", "cant"),
        "FUE-04": ("fue-04-whatsapp.csv", "WhatsApp", "pedido", "fecha", "producto", "cantidad"),
    }
    for fu, (archivo, canal_fijo, c_id, c_fecha, c_prod, c_cant) in cfg.items():
        vistas = set()
        for f in ER.leer(data / archivo):
            clave = tuple(f.values())
            dup = clave in vistas
            vistas.add(clave)
            fecha, hora = ER.fecha_texto(f[c_fecha]), ER.hora_de(f["hora"] if fu == "FUE-01" else f[c_fecha])
            cant = ER.numero(f[c_cant])
            r = {"pedido_id": f[c_id], "fuente": fu, "fecha": fecha.isoformat() if fecha else "", "hora": _hhmm(hora) if fu != "FUE-01" else (f["hora"] or ""),
                 "turno": "", "canal": canal_fijo or f["canal"], "producto": alias.get(f[c_prod], ""), "cantidad": _num(cant),
                 "precio_unitario": "", "descuento": "", "monto": "", "comision": "", "comision_pct": "", "estado": f.get("estado", ""),
                 "cliente_id": "", "es_duplicado": int(dup), "es_invalido": 0}
            if fu == "FUE-01":
                precio = ER.numero(f["precio_unitario"])
                r["precio_unitario"] = _num(precio)
                r["descuento"] = _num(ER.numero(f["descuento"]) or 0)
                r["turno"] = f["turno"] or ER.HORAS.get(hora, "")
                r["es_invalido"] = int(cant is None or cant <= 0 or precio is None)
            else:
                r["turno"] = ER.HORAS.get(hora, "")
                if fu == "FUE-02":
                    monto = ER.numero(f["monto"])
                    r["monto"], r["comision"] = _num(monto), _num(ER.numero(f["comision"]))
                    r["es_invalido"] = int(monto is None or f["estado"] == "CANCELADO")
                elif fu == "FUE-03":
                    monto = ER.numero(f["total"])
                    r["monto"], r["comision_pct"] = _num(monto), f["comision_pct"]
                    r["es_invalido"] = int(monto is None or f["estado"] == "CANCELADO")
                else:
                    monto = ER.numero(f["monto"])
                    r["monto"] = _num(monto)
                    r["es_invalido"] = int(cant is None or cant <= 0 or monto is None)
                    r["cliente_id"] = clientes.setdefault(f["telefono"], f"C-{len(clientes) + 1:04d}")
            pedidos.append(r)
    _escribir(out / "pedidos.csv", PEDIDOS, pedidos)

    # producción: sin jornadas repetidas ni imposibles
    brutas = ER.leer(data / "fue-05-produccion.csv")
    unicas, _ = ER.unicas(brutas)
    prod = []
    for f in unicas:
        prep, vend, merma = ER.numero(f["pollos_preparados"]), ER.numero(f["pollos_vendidos"]), ER.numero(f["pollos_merma"])
        if prep is None or vend is None or vend > prep:
            continue
        prod.append({"fecha": ER.fecha_texto(f["fecha"]).isoformat(), "turno": f["turno"], "pollos_preparados": _num(prep),
                     "pollos_vendidos": _num(vend), "pollos_merma": _num(merma), "responsable": f["responsable"] or "Sin dato"})
    prod.sort(key=lambda r: (r["fecha"], r["turno"]))
    _escribir(out / "produccion.csv", ["fecha", "turno", "pollos_preparados", "pollos_vendidos", "pollos_merma", "responsable"], prod)

    # precio diario completo
    precios = {ER.fecha_texto(f["fecha"]): float(f["precio_kg"]) for f in ER.leer(data / "fue-06-precios-pollo.csv")}
    d, fin, ultimo, filas = min(precios), max(precios), None, []
    while d <= fin:
        imp = d not in precios
        ultimo = precios.get(d, ultimo)
        filas.append({"fecha": d.isoformat(), "precio_kg": f"{ultimo:.2f}", "valor_imputado": int(imp)})
        d += dt.timedelta(days=1)
    _escribir(out / "precios-pollo.csv", ["fecha", "precio_kg", "valor_imputado"], filas)

    # archivos de apoyo: ya vienen limpios
    for n in ("apoyo-catalogo-productos.csv", "apoyo-costos-operativos.csv"):
        (out / n.replace("apoyo-", "")).write_bytes((data / n).read_bytes())
    validos = sum(1 for r in pedidos if not r["es_duplicado"] and not r["es_invalido"])
    return {"pedidos": len(pedidos), "duplicados": sum(r["es_duplicado"] for r in pedidos), "validos": validos,
            "produccion": len(prod), "precios": len(filas), "imputados": sum(r["valor_imputado"] for r in filas), "clientes": len(clientes),
            "sin_producto": sum(1 for r in pedidos if not r["producto"]), "sin_turno": sum(1 for r in pedidos if not r["turno"])}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=".")
    print(limpiar(ap.parse_args(argv).raiz))


if __name__ == "__main__":
    main()
