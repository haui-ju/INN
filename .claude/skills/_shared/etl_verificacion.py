#!/usr/bin/env python3
"""Comparación del ETL del equipo con la hoja de respuestas de los datos generados (data/respuestas/).

  python3 .claude/skills/_shared/etl_verificacion.py comparar [--raiz .] [--evidencia RUTA] [--actualizar]

Toma los totales del equipo de data/salida/<tabla>.csv (tablas que exporta de Power BI) o, si no hay, de `totales` de la
evidencia (ventas_total, comision_total, lineas_total), y los compara con data/respuestas/. Imprime un JSON con
{estado, fuente, diferencias}; cada diferencia trae tabla, mes, medida, esperado, obtenido, desvio y la regla probable.
Con --actualizar escribe ese resultado en `verificacion` de la evidencia. Solo biblioteca estándar.

Forma de data/salida/ (nombres de columna del modelo):
  dCalendario.csv  fecha_key, y (anio y mes) o fecha        dCanal.csv  canal_key, canal        dTurno.csv  turno_key, turno
  fPedidos.csv     fecha_key, canal_key, venta_bruta, comision [, registro_valido]
  fProduccion.csv  fecha_key, turno_key, pollos_preparados, pollos_vendidos, pollos_merma
  fPrecioInsumo.csv fecha_key, precio_kg [, valor_imputado]
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

TOL_DINERO = 0.01
VALIDO = {"1", "true", "verdadero", "si", "sí", "x"}
# Defectos que, si quedan sin tratar, explican filas de más o de menos (contratos del capítulo 3).
DE_MAS = ("duplicado", "registro_invalido")
DE_MENOS = ("nombre_producto", "formato_fecha", "nulo")


def _leer(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _num(s):
    """Número de un texto con coma o punto decimal («1 234,50», «1,234.50» y «45.5»); 0 si está vacío."""
    s = str(s or "").strip().replace(" ", "").replace(" ", "")
    if not s:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def _mes_de(fila):
    """AAAA-MM de una fila de dCalendario: por `anio` y `mes` o por `fecha` (AAAA-MM-DD o DD/MM/AAAA)."""
    a, m = str(fila.get("anio", "")).strip(), str(fila.get("mes", "")).strip()
    if a.isdigit() and m.isdigit():
        return f"{int(a):04d}-{int(m):02d}"
    f = str(fila.get("fecha", "")).strip()
    g = re.match(r"^(\d{4})-(\d{2})-\d{2}", f)
    if g:
        return f"{g.group(1)}-{g.group(2)}"
    g = re.match(r"^\d{1,2}[/-](\d{1,2})[/-](\d{4})", f)
    return f"{g.group(2)}-{int(g.group(1)):02d}" if g else ""


def esperados(raiz):
    """Lo que dejan las limpiezas correctas, de data/respuestas/ (vacío si no existe)."""
    d = Path(raiz) / "data" / "respuestas"

    def csv_de(n):
        return _leer(d / n) if (d / n).is_file() else []
    return {
        "ventas": {(r["mes"], r["canal"]): {"lineas": int(_num(r["lineas"])), "ventas": _num(r["ventas"]), "comision": _num(r["comision"])}
                   for r in csv_de("ventas-mes-canal.csv")},
        "produccion": {(r["mes"], r["turno"]): {"preparados": int(_num(r["preparados"])), "vendidos": int(_num(r["vendidos"])), "merma": int(_num(r["merma"]))}
                       for r in csv_de("produccion-mes-turno.csv")},
        "precio": {r["mes"]: {"precio_medio": _num(r["precio_medio"]), "dias_imputados": int(_num(r["dias_imputados"]))} for r in csv_de("precio-mes.csv")},
        "defectos": csv_de("defectos.csv"),
    }


def _dim(salida, nombre, clave, valor):
    f = salida / f"{nombre}.csv"
    return {r[clave]: r for r in _leer(f)} if f.is_file() else {}


def obtenidos(raiz):
    """Totales de las tablas que el equipo exportó a data/salida/ (solo las que existen)."""
    s = Path(raiz) / "data" / "salida"
    out = {"ventas": None, "produccion": None, "precio": None}
    if not s.is_dir():
        return out
    cal = {k: _mes_de(r) for k, r in _dim(s, "dCalendario", "fecha_key", None).items()}
    canal = {k: r.get("canal", "") for k, r in _dim(s, "dCanal", "canal_key", None).items()}
    turno = {k: r.get("turno", "") for k, r in _dim(s, "dTurno", "turno_key", None).items()}
    if (s / "fPedidos.csv").is_file():
        v = {}
        for r in _leer(s / "fPedidos.csv"):
            if "registro_valido" in r and str(r["registro_valido"]).strip().lower() not in VALIDO:
                continue
            k = (cal.get(r.get("fecha_key"), ""), canal.get(r.get("canal_key"), ""))
            a = v.setdefault(k, {"lineas": 0, "ventas": 0.0, "comision": 0.0})
            a["lineas"] += 1
            a["ventas"] += _num(r.get("venta_bruta"))
            a["comision"] += _num(r.get("comision"))
        out["ventas"] = v
    if (s / "fProduccion.csv").is_file():
        p = {}
        for r in _leer(s / "fProduccion.csv"):
            k = (cal.get(r.get("fecha_key"), ""), turno.get(r.get("turno_key"), ""))
            a = p.setdefault(k, {"preparados": 0, "vendidos": 0, "merma": 0})
            a["preparados"] += int(_num(r.get("pollos_preparados")))
            a["vendidos"] += int(_num(r.get("pollos_vendidos")))
            a["merma"] += int(_num(r.get("pollos_merma")))
        out["produccion"] = p
    if (s / "fPrecioInsumo.csv").is_file():
        acum = {}
        for r in _leer(s / "fPrecioInsumo.csv"):
            m = cal.get(r.get("fecha_key"), "")
            a = acum.setdefault(m, {"suma": 0.0, "n": 0, "imputados": 0})
            a["suma"] += _num(r.get("precio_kg"))
            a["n"] += 1
            a["imputados"] += int(_num(r.get("valor_imputado")))
        out["precio"] = {m: {"precio_medio": a["suma"] / a["n"] if a["n"] else 0.0, "dias_imputados": a["imputados"]} for m, a in acum.items()}
    return out


def _regla(defectos, tipos):
    reglas = [d.get("regla_sugerida", "").strip() for d in defectos if d.get("defecto") in tipos and d.get("regla_sugerida", "").strip()]
    return " o ".join(dict.fromkeys(reglas))


def regla_probable(medida, esperado, obtenido, defectos):
    """Qué regla del ETL explica probablemente la diferencia (orientación, no un diagnóstico)."""
    if medida == "lineas":
        if obtenido > esperado:
            r = _regla(defectos, DE_MAS)
            return "filas de más: quedaron duplicados o registros inválidos" + (f" (revisa: {r})" if r else "")
        r = _regla(defectos, DE_MENOS)
        return "filas de menos: alguna regla descarta filas válidas" + (f" (revisa: {r})" if r else "")
    if medida == "ventas":
        return "monto distinto: revisa el tipo numérico, los descuentos y las filas anuladas"
    if medida == "comision":
        return "comisión distinta: revisa cómo se homologa la comisión de cada aplicación"
    if medida in ("preparados", "vendidos", "merma"):
        return "producción distinta: revisa los nulos y el formato de fecha de la hoja de producción"
    r = _regla(defectos, ("dia_sin_precio",))
    return "precio distinto: revisa la imputación de los días sin precio" + (f" ({r})" if r else "")


def _difiere(medida, e, o):
    return abs(e - o) > (TOL_DINERO if medida in ("ventas", "comision", "precio_medio") else 0)


def _diferencia(tabla, mes, medida, e, o, defectos, **extra):
    d = {"tabla": tabla, "mes": mes, **extra, "medida": medida, "esperado": round(e, 2), "obtenido": round(o, 2),
         "desvio": round(o - e, 2), "regla_probable": regla_probable(medida, e, o, defectos)}
    return d


def _por_clave(tabla, medidas, esp, obt, defectos, etiqueta):
    out = []
    for (mes, otro), e in sorted(esp.items()):
        o = (obt or {}).get((mes, otro), {})
        for m in medidas:
            if _difiere(m, e[m], o.get(m, 0)):
                out.append(_diferencia(tabla, mes, m, e[m], o.get(m, 0), defectos, **{etiqueta: otro}))
    return out


def comparar(raiz, evidencia=None):
    """{estado, fuente, diferencias}: totales del equipo (data/salida/ o `totales` de la evidencia) contra data/respuestas/."""
    esp = esperados(raiz)
    if not (esp["ventas"] or esp["produccion"] or esp["precio"]):
        return {"estado": "sin_respuestas", "fuente": None, "diferencias": []}
    obt = obtenidos(raiz)
    dif, fuente = [], "salida"
    if obt["ventas"] is not None:
        dif += _por_clave("fPedidos", ("lineas", "ventas", "comision"), esp["ventas"], obt["ventas"], esp["defectos"], "canal")
    if obt["produccion"] is not None:
        dif += _por_clave("fProduccion", ("preparados", "vendidos", "merma"), esp["produccion"], obt["produccion"], esp["defectos"], "turno")
    if obt["precio"] is not None:
        for mes, e in sorted(esp["precio"].items()):
            o = obt["precio"].get(mes, {})
            for m in ("precio_medio", "dias_imputados"):
                if _difiere(m, e[m], o.get(m, 0)):
                    dif.append(_diferencia("fPrecioInsumo", mes, m, e[m], o.get(m, 0), esp["defectos"]))
    if obt["ventas"] is None and obt["produccion"] is None and obt["precio"] is None:
        fuente = "totales"
        t = (evidencia or {}).get("totales") or {}
        if not t:
            return {"estado": "sin_datos_del_equipo", "fuente": None, "diferencias": []}
        suma = {"lineas": sum(v["lineas"] for v in esp["ventas"].values()), "ventas": sum(v["ventas"] for v in esp["ventas"].values()),
                "comision": sum(v["comision"] for v in esp["ventas"].values())}
        clave = {"lineas": "lineas_total", "ventas": "ventas_total", "comision": "comision_total"}
        for m in ("lineas", "ventas", "comision"):
            if clave[m] in t and _difiere(m, suma[m], _num(t[clave[m]])):
                dif.append(_diferencia("fPedidos", "total", m, suma[m], _num(t[clave[m]]), esp["defectos"]))
    return {"estado": "diferencias" if dif else "coincide", "fuente": fuente, "diferencias": dif}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0].startswith("-"):
        argv = ["comparar", *argv]  # datagen.py verificar llama main(["--raiz", raiz])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("comparar")
    c.add_argument("--raiz", default=".")
    c.add_argument("--evidencia")
    c.add_argument("--actualizar", action="store_true", help="escribe el resultado en `verificacion` de la evidencia")
    a = ap.parse_args(argv)
    ev, ruta = None, Path(a.evidencia) if a.evidencia else None
    if ruta and ruta.is_file():
        ev = json.loads(ruta.read_text(encoding="utf-8"))
    res = comparar(Path(a.raiz).resolve(), ev)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if a.actualizar:
        if ev is None:
            print("ERROR: --actualizar necesita --evidencia con un archivo existente", file=sys.stderr)
            return 1
        ev["verificacion"] = {"estado": res["estado"], "diferencias": res["diferencias"]}
        ruta.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if res["estado"] in ("coincide", "diferencias") else 1


if __name__ == "__main__":
    sys.exit(main())
