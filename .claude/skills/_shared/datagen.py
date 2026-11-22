#!/usr/bin/env python3
"""Generador de los datos del proyecto (08-make-etl): las fuentes del brief en CSV, reproducibles y calibradas con el informe.

  python3 .claude/skills/_shared/datagen.py parametros [--raiz .]               (deriva data/parametros.json del brief y del informe)
  python3 .claude/skills/_shared/datagen.py generar    [--raiz .] [--confirmar]  (sin --confirmar solo muestra los parámetros)
  python3 .claude/skills/_shared/datagen.py verificar  [--raiz .]               (compara los totales del equipo con data/respuestas/)

Con la misma semilla y los mismos parámetros produce archivos idénticos byte a byte. Solo biblioteca estándar.
Los datos son generados para el proyecto: se declaran como tales en data/README.md y en la sección 3.1 del informe.
"""
import argparse
import csv
import datetime as dt
import json
import math
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
CANALES = ["Salón", "Para llevar", "WhatsApp", "Rappi", "PedidosYa"]
TURNOS = ["Mañana", "Tarde", "Noche"]
APPS = ("Rappi", "PedidosYa")
# (hora de inicio y fin de cada turno, peso del turno en las ventas)
HORAS = {"Mañana": range(11, 15), "Tarde": range(15, 19), "Noche": range(19, 23)}
PESO_HORA = {11: 3, 12: 7, 13: 10, 14: 8, 15: 4, 16: 3, 17: 3, 18: 4, 19: 8, 20: 10, 21: 8, 22: 4}
SEMANA = [0.78, 0.72, 0.85, 0.90, 1.12, 1.30, 1.45]          # lunes a domingo
ESTACION = {1: 0.95, 2: 0.92, 3: 0.97, 4: 0.98, 5: 1.00, 6: 1.00, 7: 1.04, 8: 1.00, 9: 1.00, 10: 1.02, 11: 1.03, 12: 1.12}
MERMA_SEMANA = [0.070, 0.115, 0.070, 0.070, 0.060, 0.055, 0.030]   # los martes sobra pollo y los domingos falta
RESPONSABLES = ["Carlos Mamani", "Rosa Quispe", "Luis Huamán"]

# producto, categoría, precio de lista, pollos equivalentes, kg de pollo vivo, otros insumos, alias que usan las fuentes
CATALOGO = [
    ("Pollo entero a la brasa", "Pollo", 62.0, 1.00, 1.90, 9.0, ["POLLO ENTERO", "Pollo entero", "Pollo a la brasa entero"]),
    ("Medio pollo a la brasa", "Pollo", 34.0, 0.50, 0.95, 5.5, ["1/2 pollo", "Medio pollo", "1/2 Pollo a la brasa"]),
    ("Cuarto de pollo con papas", "Pollo", 19.0, 0.25, 0.48, 3.5, ["1/4 pollo c/ papas", "Cuarto pollo", "1/4 Pollo + papas"]),
    ("Combo familiar", "Combos", 78.0, 1.00, 1.90, 14.0, ["COMBO FAMILIAR", "Combo fam.", "Combo familiar (pollo, papas y bebida)"]),
    ("Parrilla personal", "Parrillas", 32.0, 0.00, 0.00, 13.0, ["PARRILLA PERSONAL", "Parrilla pers.", "Parrilla 1 persona"]),
    ("Parrilla familiar", "Parrillas", 85.0, 0.00, 0.00, 36.0, ["PARRILLA FAMILIAR", "Parrilla fam.", "Parrilla 4 personas"]),
    ("Bebida", "Bebidas", 9.0, 0.00, 0.00, 3.2, ["Gaseosa 1.5 L", "Chicha morada", "BEBIDA"]),
    ("Adicional", "Adicionales", 7.0, 0.00, 0.00, 2.2, ["Papas fritas", "Ensalada", "ADICIONAL"]),
]
PRINCIPALES = [0, 1, 2, 3, 4, 5]
MEZCLA = {  # peso de cada principal por canal
    "Salón": [0.18, 0.26, 0.28, 0.10, 0.09, 0.09],
    "Para llevar": [0.20, 0.27, 0.32, 0.11, 0.05, 0.05],
    "WhatsApp": [0.22, 0.22, 0.20, 0.20, 0.08, 0.08],
    "Rappi": [0.14, 0.24, 0.34, 0.20, 0.05, 0.03],
    "PedidosYa": [0.14, 0.24, 0.34, 0.20, 0.05, 0.03],
}
PROB_ALIAS = {"fue-01": 0.12, "fue-02": 0.60, "fue-03": 0.60, "fue-04": 0.30}


class ErrorDatos(Exception):
    """Los datos generados quedan fuera de las tolerancias declaradas o faltan parámetros."""


# ------------------------------------------------------------------ parámetros
def _fecha(s):
    return dt.date.fromisoformat(s)


def _meses(inicio, fin):
    a, b = _fecha(inicio), _fecha(fin)
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def parametros_base():
    return {
        "schema": 1,
        "semilla": 2026,
        "periodo": {"inicio": "2025-08-01", "fin": "2026-10-31"},
        "locales": 1,
        "ventas_anuales_uit": 436,
        "valor_uit": 5500,
        "ventas_anuales": 2400000,
        "canales": [
            {"nombre": "Salón", "comision_pct": 0, "participacion_inicial": 0.39, "participacion_final": 0.28},
            {"nombre": "Para llevar", "comision_pct": 0, "participacion_inicial": 0.36, "participacion_final": 0.25},
            {"nombre": "WhatsApp", "comision_pct": 0, "participacion_inicial": 0.10, "participacion_final": 0.12},
            {"nombre": "Rappi", "comision_pct": 30, "participacion_inicial": 0.09, "participacion_final": 0.20},
            {"nombre": "PedidosYa", "comision_pct": 25, "participacion_inicial": 0.06, "participacion_final": 0.15},
        ],
        "productos": [{"nombre": p[0], "categoria": p[1], "precio": p[2], "costo": round(p[4] * 6.10 + p[5], 2)} for p in CATALOGO],
        "merma_pct": 7.0,
        "margen_neto": {"inicial": 14.0, "final": 8.0},
        "precio_pollo": {"inicial": 6.10, "julio_antes": 6.10, "julio_despues": 6.90},
        "crecimiento_interanual": 18.0,
        "tolerancias": {"margen_neto_pp": 0.5, "merma_pp": 0.4, "participacion_apps_pp": 2.0, "crecimiento_pp": 2.5, "ventas_anuales_pct": 5.0,
                        "calidad_minima": 97.5, "calidad_maxima": 99.5},
        "origen": {},
    }


def _texto_vigente(raiz, paso, archivo):
    try:
        import projectcfg as P
        cfg = P.load(raiz)
        e = cfg["pasos"].get(paso)
        d = P.run_dir(paso, e["run"], raiz) if e and e.get("run") else None
        f = d / archivo if d else None
        return f.read_text(encoding="utf-8") if f and f.is_file() else ""
    except Exception:  # sin config o sin corrida: se usan los valores base
        return ""


def derivar_parametros(raiz="."):
    """Parámetros tomados del brief y del informe vigentes; lo que no se encuentre queda con el valor base y su origen."""
    p = parametros_base()
    o = p["origen"]
    brief = _texto_vigente(raiz, "01-make-project-brief", "brief.md")
    m = re.search(r"de (\w+) de (\d{4}) a (\w+) de (\d{4})", brief)
    if m and m.group(1).lower() in MESES and m.group(3).lower() in MESES:
        a, b = (int(m.group(2)), MESES.index(m.group(1).lower()) + 1), (int(m.group(4)), MESES.index(m.group(3).lower()) + 1)
        fin = dt.date(b[0] + (b[1] == 12), 1 if b[1] == 12 else b[1] + 1, 1) - dt.timedelta(days=1)
        p["periodo"] = {"inicio": f"{a[0]}-{a[1]:02d}-01", "fin": fin.isoformat()}
        o["periodo"] = "brief: alcance y FUE-01"
    t13 = _texto_vigente(raiz, "03-make-business-diagnosis", "secciones/1.3.md")
    m = re.search(r"ventas anuales de S/ ([\d  ]+)", t13)
    if m:
        p["ventas_anuales"] = int(re.sub(r"\D", "", m.group(1)))
        o["ventas_anuales"] = "informe: sección 1.3"
    m = re.search(r"unas (\d+) UIT", t13)
    if m:
        p["ventas_anuales_uit"] = int(m.group(1))
    m = re.search(r"UIT de referencia \| S/ ([\d  ]+)", t13)
    if m:
        p["valor_uit"] = int(re.sub(r"\D", "", m.group(1)))
    for k in ("margen_neto", "merma_pct", "precio_pollo", "crecimiento_interanual", "canales"):
        o.setdefault(k, "informe: secciones 1.4, 1.5, 1.7 y 1.8 (valor base si no se pudo leer)")
    return p


def ruta_datos(raiz="."):
    return Path(raiz) / "data"


def leer_parametros(raiz="."):
    f = ruta_datos(raiz) / "parametros.json"
    if not f.is_file():
        raise ErrorDatos(f"falta {f}: ejecuta `datagen.py parametros` y confírmalo con el usuario")
    return json.loads(f.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ simulación
def _dias(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def _precios(params, rng):
    """(precio publicado por día, con huecos; precio efectivo, con el último disponible; días sin precio)."""
    a, b = _fecha(params["periodo"]["inicio"]), _fecha(params["periodo"]["fin"])
    pp = params["precio_pollo"]
    j1, j14 = dt.date(2026, 7, 1), dt.date(2026, 7, 14)
    dias = list(_dias(a, b))
    ruido, serie = 0.0, {}
    for d in dias:
        ruido = 0.85 * ruido + rng.gauss(0, 0.045)
        if d <= j1:
            base = pp["julio_antes"]
        elif d < j14:
            base = pp["julio_antes"] + (pp["julio_despues"] - pp["julio_antes"]) * (d - j1).days / (j14 - j1).days
        else:
            base = pp["julio_despues"]
        extra = 0.0 if d in (j1, j14) else max(-0.18, min(0.18, ruido))
        serie[d] = round(base + extra, 2)
    faltan = [d for d in dias if d not in (a, b, j1, j14) and (rng.random() < 0.022 or (d.weekday() == 6 and rng.random() < 0.06))]
    faltan_set, efectiva, ultimo = set(faltan), {}, None
    for d in dias:
        if d not in faltan_set:
            ultimo = serie[d]
        efectiva[d] = ultimo if ultimo is not None else serie[d]
    return {d: v for d, v in serie.items() if d not in faltan_set}, efectiva, faltan


def _lineas_limpias(params, rng, meses):
    """Líneas de venta por mes y canal: por cada mes y canal se arman tickets hasta alcanzar su venta objetivo."""
    n = len(meses)
    g = (1 + params["crecimiento_interanual"] / 100) ** (1 / 12)
    pesos = [g ** i * ESTACION[m] for i, (_, m) in enumerate(meses)]
    ultimos = pesos[-12:]
    escala = params["ventas_anuales"] / (sum(ultimos) * (12 / len(ultimos)))
    canales = {c["nombre"]: c for c in params["canales"]}
    lineas, t = [], 0
    for i, (y, m) in enumerate(meses):
        dias = list(_dias(dt.date(y, m, 1), dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1) - dt.timedelta(days=1)))
        w_dia = [SEMANA[d.weekday()] * rng.lognormvariate(0, 0.10) for d in dias]
        f = i / (n - 1) if n > 1 else 0.0
        for c in CANALES:
            ch = canales[c]
            share = ch["participacion_inicial"] + (ch["participacion_final"] - ch["participacion_inicial"]) * f
            objetivo, acum = escala * pesos[i] * share, 0.0
            while acum < objetivo:
                t += 1
                d = rng.choices(dias, w_dia)[0]
                hora = rng.choices(list(PESO_HORA), list(PESO_HORA.values()))[0]
                minuto = rng.randrange(60)
                cesta = {}      # un producto aparece una sola vez por ticket: así un duplicado exacto siempre es un defecto
                for _ in range(1 + (rng.random() < 0.30)):
                    k = rng.choices(PRINCIPALES, MEZCLA[c])[0]
                    cesta[k] = cesta.get(k, 0) + 1 + (k in (0, 3) and rng.random() < 0.25)
                if rng.random() < 0.72:
                    cesta[6] = 1 + (rng.random() < 0.5) + (rng.random() < 0.2)
                if rng.random() < 0.50:
                    cesta[7] = 1 + (rng.random() < 0.4)
                for k, q in cesta.items():
                    venta = round(CATALOGO[k][2] * q, 2)
                    acum += venta
                    lineas.append({"t": t, "canal": c, "fecha": d, "hora": hora, "min": minuto, "k": k, "cant": q, "venta": venta,
                                   "mes": f"{y}-{m:02d}", "turno": _turno(hora)})
    return sorted(lineas, key=lambda x: (x["fecha"], x["hora"], x["min"], x["t"]))


def _turno(hora):
    return next(t for t, hs in HORAS.items() if hora in hs)


def m2(x):
    return f"{x:.2f}"


FUENTE_DE = {"Salón": "fue-01", "Para llevar": "fue-01", "WhatsApp": "fue-04", "Rappi": "fue-02", "PedidosYa": "fue-03"}
PREFIJO = {"Salón": "T", "Para llevar": "T", "WhatsApp": "WA", "Rappi": "RP", "PedidosYa": "PY"}
P_DUPLICADO = {"fue-01": 0.005, "fue-02": 0.012, "fue-03": 0.012, "fue-04": 0.010}
FORMATOS = {"fue-01": ("%Y-%m-%d", "%d/%m/%Y"), "fue-02": ("%Y-%m-%d", "%d/%m/%Y"), "fue-03": ("%d/%m/%Y", "%Y-%m-%d"), "fue-04": ("%Y-%m-%d", "%d/%m/%Y")}


def _fuentes(params, rng, lineas, efectivo):
    """Filas brutas de las cuatro fuentes de ventas con sus defectos, y el registro de cuáles son válidas."""
    comision = {c["nombre"]: c["comision_pct"] / 100 for c in params["canales"]}
    defectos, filas, regs = {}, {f: [] for f in P_DUPLICADO}, []
    telefonos = [f"9{rng.randrange(10 ** 8):08d}" for _ in range(900)]
    cliente = {}

    def cuenta(fu, d):
        defectos[(fu, d)] = defectos.get((fu, d), 0) + 1

    for l in lineas:
        fu, k = FUENTE_DE[l["canal"]], CATALOGO[l["k"]]
        base, alt = FORMATOS[fu]
        l["costo"] = round(l["cant"] * (k[4] * efectivo[l["fecha"]] + k[5]), 4)
        r, valido = rng.random(), True
        cant, monto, desc, cancelado = l["cant"], l["venta"], 0, False
        if r < (0.007 if fu == "fue-01" else 0.006):          # inválido: cantidad nula o monto vacío
            valido = False
            cuenta(fu, "registro_invalido")
            if fu in ("fue-01", "fue-04") and rng.random() < 0.5:
                cant = rng.choice([0, ""])
            else:
                monto = ""
        elif fu in ("fue-02", "fue-03") and r < 0.009:         # pedido cancelado que el reporte de la aplicación incluye
            valido, cancelado = False, True
            cuenta(fu, "registro_invalido")
        elif fu == "fue-01" and rng.random() < 0.03:
            desc = round(l["venta"] * 0.10, 2)
        l["neta"] = round(l["venta"] - desc, 2)
        l["comision"] = round(l["neta"] * comision[l["canal"]], 2)
        d = l["fecha"].strftime(alt) if rng.random() < 0.04 else l["fecha"].strftime(base)
        if d != l["fecha"].strftime(base):
            cuenta(fu, "formato_fecha")
        producto = rng.choice(k[6]) if rng.random() < PROB_ALIAS.get(fu, 0.0) else k[0]
        if producto != k[0]:
            cuenta(fu, "nombre_producto")
        pid = f"{PREFIJO[l['canal']]}-{l['t']:06d}"
        hm = f"{l['hora']:02d}:{l['min']:02d}"
        if fu == "fue-01":
            turno = l["turno"]
            if rng.random() < 0.01:
                turno = ""
                cuenta(fu, "nulo")
            precio = CATALOGO[l["k"]][2] if monto != "" else ""
            fila = [pid, d, hm, turno, l["canal"], producto, cant, precio, desc if desc else 0, "OK"]
            if valido and rng.random() < 0.02 and not desc:
                fila[8] = ""
                cuenta(fu, "nulo")
        elif fu == "fue-02":
            com = m2(l["comision"]) if monto != "" else ""
            fila = [pid, f"{d} {hm}:00", producto, cant, m2(monto) if monto != "" else "", com, "CANCELADO" if cancelado else "ENTREGADO"]
        elif fu == "fue-03":
            fila = [pid, f"{d} {hm}", producto, cant, m2(monto) if monto != "" else "", int(comision["PedidosYa"] * 100), "CANCELADO" if cancelado else "ENTREGADO"]
        else:
            tel = cliente.setdefault(l["t"], rng.choice(telefonos))
            fila = [pid, f"{d} {hm}", tel, producto, cant, m2(monto) if monto != "" else "", rng.choice(["Delivery", "Delivery", "Recojo"])]
        filas[fu].append(fila)
        regs.append({"fu": fu, "mes": l["mes"], "valido": valido, "l": l if valido else None})
        if rng.random() < P_DUPLICADO[fu]:
            filas[fu].append(list(fila))
            cuenta(fu, "duplicado")
            regs.append({"fu": fu, "mes": l["mes"], "valido": False, "l": None})
    return filas, regs, defectos


def _produccion(params, rng, lineas, a, b):
    """Producción por día y turno a partir de lo vendido: la merma sigue el patrón semanal y se ajusta al promedio del informe."""
    vendido = {}
    for l in lineas:
        vendido[(l["fecha"], l["turno"])] = vendido.get((l["fecha"], l["turno"]), 0.0) + CATALOGO[l["k"]][3] * l["cant"]
    claves = [(d, t) for d in _dias(a, b) for t in TURNOS]
    ruido = {c: rng.lognormvariate(0, 0.25) for c in claves}
    objetivo = params["merma_pct"] / 100

    def armar(k):
        out = []
        for d, t in claves:
            v = int(round(vendido.get((d, t), 0.0)))
            m = max(0.0, min(0.30, MERMA_SEMANA[d.weekday()] * k * ruido[(d, t)]))
            prep = int(math.ceil(v / (1 - m))) if v else 0
            out.append((d, t, prep, v, prep - v))
        return out

    lo, hi = 0.2, 2.5
    for _ in range(40):
        k = (lo + hi) / 2
        filas = armar(k)
        prep = sum(f[2] for f in filas)
        if (sum(f[4] for f in filas) / prep if prep else 0) < objetivo:
            lo = k
        else:
            hi = k
    return armar((lo + hi) / 2)


def _fila_produccion(f, rng, defectos, regs):
    d, t, prep, v, mer = f
    base, alt = FORMATOS["fue-01"]
    fecha = d.strftime(base)
    if rng.random() < 0.03:
        fecha = d.strftime(alt)
        defectos[("fue-05", "formato_fecha")] = defectos.get(("fue-05", "formato_fecha"), 0) + 1
    resp = RESPONSABLES[d.weekday() % len(RESPONSABLES)]
    if rng.random() < 0.01:
        resp = ""
        defectos[("fue-05", "nulo")] = defectos.get(("fue-05", "nulo"), 0) + 1
    valido = True
    if rng.random() < 0.004:                      # vendidos mayores que preparados
        valido = False
        defectos[("fue-05", "registro_invalido")] = defectos.get(("fue-05", "registro_invalido"), 0) + 1
        fila = [fecha, t, prep, prep + 3 + int(rng.random() * 4), 0, resp]
    else:
        fila = [fecha, t, prep, v, mer, resp]
    regs.append({"fu": "fue-05", "mes": f"{d.year}-{d.month:02d}", "valido": valido, "p": (d, t, prep, v, mer) if valido else None})
    out = [fila]
    if rng.random() < 0.004:
        out.append(list(fila))
        defectos[("fue-05", "duplicado")] = defectos.get(("fue-05", "duplicado"), 0) + 1
        regs.append({"fu": "fue-05", "mes": f"{d.year}-{d.month:02d}", "valido": False, "p": None})
    return out


REGLAS = {
    "registro_invalido": "Excluir las filas con cantidad o monto nulos o en cero y los pedidos cancelados",
    "duplicado": "Quitar los duplicados exactos por identificador de pedido y producto",
    "nombre_producto": "Homologar el nombre contra el catálogo de productos (apoyo-catalogo-productos.csv)",
    "formato_fecha": "Convertir todas las fechas al formato único AAAA-MM-DD (las que tienen barras son día/mes/año)",
    "nulo": "Completar el turno desde la hora y el descuento con 0; el resto se marca como dato faltante",
    "dia_sin_precio": "Imputar el último precio disponible y marcar el día como imputado",
}
# Textos propios de una fuente cuando la regla general no describe su defecto
REGLAS_FUENTE = {
    ("fue-01", "nulo"): "Completar el turno vacío desde la hora de la venta y tomar el descuento vacío como 0",
    ("fue-05", "nulo"): "Completar el responsable vacío con «Sin dato» (no afecta a ningún KPI)",
    ("fue-05", "registro_invalido"): "Excluir las jornadas donde los pollos vendidos superan a los preparados",
    ("fue-05", "duplicado"): "Quitar las jornadas repetidas (misma fecha y turno)",
    ("fue-02", "registro_invalido"): "Excluir los pedidos CANCELADOS y las filas sin monto",
    ("fue-03", "registro_invalido"): "Excluir los pedidos CANCELADOS y las filas sin total",
    ("fue-04", "registro_invalido"): "Excluir las filas con cantidad 0 o vacía o sin monto",
    ("fue-01", "registro_invalido"): "Excluir las filas con cantidad 0 o vacía o sin precio unitario",
}
TIPOS = list(REGLAS)


def _pct(a, b):
    return 100.0 * a / b if b else 0.0


def simular(params):
    """Simula todo el caso y devuelve las filas de cada archivo, la hoja de respuestas y el resumen calibrado (sin escribir nada)."""
    rng = random.Random(params["semilla"])
    a, b = _fecha(params["periodo"]["inicio"]), _fecha(params["periodo"]["fin"])
    meses = _meses(params["periodo"]["inicio"], params["periodo"]["fin"])
    nombres = [f"{y}-{m:02d}" for y, m in meses]
    publicados, efectivo, sin_precio = _precios(params, rng)
    lineas = _lineas_limpias(params, rng, meses)
    filas, regs, defectos = _fuentes(params, rng, lineas, efectivo)
    prod = _produccion(params, rng, lineas, a, b)
    filas["fue-05"] = []
    for f in prod:
        filas["fue-05"] += _fila_produccion(f, rng, defectos, regs)
    base, alt = FORMATOS["fue-01"]
    filas["fue-06"] = []
    for d in sorted(publicados):
        if rng.random() < 0.03:
            filas["fue-06"].append([d.strftime(alt), m2(publicados[d])])
            defectos[("fue-06", "formato_fecha")] = defectos.get(("fue-06", "formato_fecha"), 0) + 1
        else:
            filas["fue-06"].append([d.strftime(base), m2(publicados[d])])
        regs.append({"fu": "fue-06", "mes": f"{d.year}-{d.month:02d}", "valido": True})
    if sin_precio:
        defectos[("fue-06", "dia_sin_precio")] = len(sin_precio)

    # hoja de respuestas: solo filas válidas y sin duplicar
    ventas = {}
    for r in regs:
        if r["valido"] and r.get("l"):
            l = r["l"]
            v = ventas.setdefault((l["mes"], l["canal"]), {"lineas": 0, "ventas": 0.0, "comision": 0.0, "costo": 0.0})
            v["lineas"] += 1
            v["ventas"] += l["neta"]
            v["comision"] += l["comision"]
            v["costo"] += l["costo"]
    por_producto = {}
    for rg in regs:
        if rg["valido"] and rg.get("l"):
            l = rg["l"]
            x = por_producto.setdefault((l["mes"], l["canal"], CATALOGO[l["k"]][0]), [0, 0.0, 0.0, 0.0])
            x[0] += 1
            x[1] += l["neta"]
            x[2] += l["comision"]
            x[3] += l["costo"]
    por_mes = {n: {"v": 0.0, "c": 0.0, "k": 0.0, "apps": 0.0} for n in nombres}
    for (mes, canal), v in ventas.items():
        por_mes[mes]["v"] += v["ventas"]
        por_mes[mes]["c"] += v["comision"]
        por_mes[mes]["k"] += v["costo"]
        if canal in APPS:
            por_mes[mes]["apps"] += v["ventas"]
    n = len(nombres)
    mn = params["margen_neto"]
    ruido_m = [0.0] + [rng.uniform(-0.35, 0.35) for _ in range(n - 2)] + [0.0] if n > 1 else [0.0]
    objetivo_margen = [mn["inicial"] + (mn["final"] - mn["inicial"]) * (i / (n - 1) if n > 1 else 0) + ruido_m[i] for i in range(n)]
    operativo = {}
    for i, mes in enumerate(nombres):
        v = por_mes[mes]
        operativo[mes] = round(v["v"] * (1 - objetivo_margen[i] / 100) - v["c"] - v["k"])
    prod_mes = {}
    for r in regs:
        if r["fu"] == "fue-05" and r["valido"]:
            d, t, prep, v, mer = r["p"]
            x = prod_mes.setdefault((r["mes"], t), [0, 0, 0])
            x[0] += prep
            x[1] += v
            x[2] += mer
    precio_mes = {}
    for d, p in efectivo.items():
        x = precio_mes.setdefault(f"{d.year}-{d.month:02d}", [0.0, 0, 0])
        x[0] += p
        x[1] += 1
        x[2] += d in set(sin_precio)
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    validas_prod = sorted(rg["p"] for rg in regs if rg["fu"] == "fue-05" and rg["valido"])
    dia_semana = {}
    for d, t, prep, v, mer in validas_prod:
        x = dia_semana.setdefault(d.weekday(), [0, 0, 0])
        x[0] += prep
        x[1] += v
        x[2] += mer
    dia_semana = [[dias[k], *x, round(_pct(x[2], x[0]), 2)] for k, x in sorted(dia_semana.items())]
    historia, pronostico, mape = {}, [], {}
    for d, t, prep, v, mer in validas_prod:
        h = historia.setdefault((d.weekday(), t), [])
        if len(h) >= 4 and v > 0:
            f = sum(h[-4:]) / 4
            e = 100 * abs(v - f) / v
            pronostico.append([d.isoformat(), t, v, round(f, 2), round(e, 2)])
            mape.setdefault(f"{d.year}-{d.month:02d}", []).append(e)
        h.append(v)
    precio_dia = [[d.isoformat(), m2(p), int(d in set(sin_precio))] for d, p in sorted(efectivo.items())]
    brutas = {f: len(v) for f, v in filas.items()}
    validas = {f: sum(1 for r in regs if r["fu"] == f and r["valido"]) for f in filas}
    kpi = []
    for i, mes in enumerate(nombres):
        v = por_mes[mes]
        ventas_fu = ("fue-01", "fue-02", "fue-03", "fue-04")      # KPI-01 se mide en fPedidos: solo las fuentes de ventas
        bm = sum(1 for r in regs if r["mes"] == mes and r["fu"] in ventas_fu)
        vm = sum(1 for r in regs if r["mes"] == mes and r["fu"] in ventas_fu and r["valido"])
        pm = [x for (m, t), x in prod_mes.items() if m == mes]
        kpi += [("KPI-01", mes, round(_pct(vm, bm), 2), "%"),
                ("KPI-02", mes, round(_pct(v["v"] - v["c"] - v["k"], v["v"]), 2), "%"),
                ("KPI-03", mes, round(objetivo_margen[i], 2), "%"),
                ("KPI-04", mes, round(_pct(sum(x[2] for x in pm), sum(x[0] for x in pm)), 2), "%"),
                ("KPI-05", mes, round(sum(mape[mes]) / len(mape[mes]), 2) if mape.get(mes) else "", "%"),
                ("KPI-06", mes, round(precio_mes[mes][0] / precio_mes[mes][1], 2), "S/ por kg")]
    resumen = {
        "meses": nombres, "lineas_limpias": len(lineas), "filas_brutas": brutas, "filas_validas": validas,
        "ventas_mes": {m: round(por_mes[m]["v"], 2) for m in nombres}, "margen_neto": [round(x, 2) for x in objetivo_margen],
        "participacion_apps": [round(_pct(por_mes[m]["apps"], por_mes[m]["v"]), 2) for m in nombres],
        "costo_operativo_pct": [round(_pct(operativo[m], por_mes[m]["v"]), 2) for m in nombres],
        "defectos": {f"{f}/{d}": c for (f, d), c in sorted(defectos.items())},
    }
    prep = sum(x[0] for x in prod_mes.values())
    resumen["merma_pct"] = round(_pct(sum(x[2] for x in prod_mes.values()), prep), 2)
    resumen["calidad_pct"] = round(_pct(sum(validas.values()), sum(brutas.values())), 2)
    if n >= 15:
        resumen["crecimiento_pct"] = round(100 * (sum(por_mes[m]["v"] for m in nombres[-3:]) / sum(por_mes[m]["v"] for m in nombres[-15:-12]) - 1), 2)
    resumen["ventas_ultimos_12"] = round(sum(por_mes[m]["v"] for m in nombres[-12:]), 2)
    resumen["precio_1_julio"] = publicados.get(dt.date(2026, 7, 1))
    resumen["precio_14_julio"] = publicados.get(dt.date(2026, 7, 14))
    resumen["dias_sin_precio"] = len(sin_precio)
    resumen["calibracion"] = calibracion(params, resumen)
    return {"por_producto": por_producto, "dia_semana": dia_semana, "pronostico": pronostico, "precio_dia": precio_dia,
            "filas": filas, "ventas": ventas, "operativo": operativo, "produccion": prod_mes, "precio_mes": precio_mes, "defectos": defectos,
            "kpi": kpi, "resumen": resumen, "nombres": nombres}


def calibracion(params, r):
    """[(cifra, esperado, obtenido, tolerancia, ok)] de las cifras que el informe afirma."""
    t, mn = params["tolerancias"], params["margen_neto"]
    ap0 = sum(c["participacion_inicial"] for c in params["canales"] if c["nombre"] in APPS) * 100
    ap1 = sum(c["participacion_final"] for c in params["canales"] if c["nombre"] in APPS) * 100
    out = []

    def chk(nombre, esperado, obtenido, tol):
        out.append((nombre, esperado, obtenido, tol, abs(obtenido - esperado) <= tol))

    chk("margen neto del primer mes (%)", mn["inicial"], r["margen_neto"][0], t["margen_neto_pp"])
    chk("margen neto del último mes (%)", mn["final"], r["margen_neto"][-1], t["margen_neto_pp"])
    chk("participación de las aplicaciones, primer mes (%)", ap0, r["participacion_apps"][0], t["participacion_apps_pp"])
    chk("participación de las aplicaciones, último mes (%)", ap1, r["participacion_apps"][-1], t["participacion_apps_pp"])
    chk("merma de lo preparado (%)", params["merma_pct"], r["merma_pct"], t["merma_pp"])
    chk("ventas de los últimos 12 meses (S/)", params["ventas_anuales"], r["ventas_ultimos_12"], params["ventas_anuales"] * t["ventas_anuales_pct"] / 100)
    if "crecimiento_pct" in r:
        chk("crecimiento interanual de las ventas (%)", params["crecimiento_interanual"], r["crecimiento_pct"], t["crecimiento_pp"])
    if r["precio_1_julio"] is not None:
        chk("precio del pollo vivo el 1 de julio de 2026 (S/ por kg)", params["precio_pollo"]["julio_antes"], r["precio_1_julio"], 0.005)
        chk("precio del pollo vivo el 14 de julio de 2026 (S/ por kg)", params["precio_pollo"]["julio_despues"], r["precio_14_julio"], 0.005)
    out.append(("calidad de datos (% de registros válidos)", f"{t['calidad_minima']} a {t['calidad_maxima']}", r["calidad_pct"], 0,
                t["calidad_minima"] <= r["calidad_pct"] <= t["calidad_maxima"]))
    op = r["costo_operativo_pct"]
    out.append(("costo operativo mensual (% de las ventas)", "25 a 55", f"{min(op)} a {max(op)}", 0, 25 <= min(op) and max(op) <= 55))
    faltan = [d for d in TIPOS if not any(k.endswith("/" + d) for k in r["defectos"])]
    out.append(("tipos de defecto presentes", len(TIPOS), len(TIPOS) - len(faltan), 0, not faltan))
    return out


# ------------------------------------------------------------------ escritura
def _escribir(ruta, cabecera, filas):
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cabecera)
        w.writerows(filas)


CABECERAS = {
    "fue-01": ("fue-01-caja.csv", ["ticket_id", "fecha", "hora", "turno", "canal", "producto", "cantidad", "precio_unitario", "descuento", "estado"]),
    "fue-02": ("fue-02-rappi.csv", ["pedido_id", "fecha_hora", "producto", "cantidad", "monto", "comision", "estado"]),
    "fue-03": ("fue-03-pedidosya.csv", ["nro_pedido", "fecha", "item", "cant", "total", "comision_pct", "estado"]),
    "fue-04": ("fue-04-whatsapp.csv", ["pedido", "fecha", "telefono", "producto", "cantidad", "monto", "tipo_entrega"]),
    "fue-05": ("fue-05-produccion.csv", ["fecha", "turno", "pollos_preparados", "pollos_vendidos", "pollos_merma", "responsable"]),
    "fue-06": ("fue-06-precios-pollo.csv", ["fecha", "precio_kg"]),
}

README = """# Datos del proyecto

**Estos datos son generados** para el proyecto (`modo_datos: generado`): no provienen de una empresa real. Se calibraron con las cifras
del informe y se generan con una semilla fija, de modo que se pueden regenerar con `python3 .claude/skills/_shared/datagen.py generar`.
Esta carpeta no se versiona en git, salvo este archivo y `parametros.json`.

Semilla: {semilla}. Periodo: {inicio} a {fin}.

| Archivo | Contenido |
|---|---|
| `fue-01-caja.csv` | Líneas de venta del salón y para llevar (FUE-01) |
| `fue-02-rappi.csv` | Reporte de Rappi (FUE-02) |
| `fue-03-pedidosya.csv` | Reporte de PedidosYa (FUE-03), con nombres de columna distintos; la fecha lleva la hora |
| `fue-04-whatsapp.csv` | Pedidos del delivery propio (FUE-04), con el teléfono del cliente; la fecha lleva la hora |
| `fue-05-produccion.csv` | Producción por día y turno (FUE-05) |
| `fue-06-precios-pollo.csv` | Precio diario del pollo vivo (FUE-06); faltan algunos días |
| `apoyo-catalogo-productos.csv` | Lista de precios y receta de cada producto, con los nombres alternativos que usan las fuentes |
| `apoyo-costos-operativos.csv` | Costo operativo de cada mes (planilla, alquiler, servicios y otros) |
| `respuestas/` | Totales esperados tras una limpieza correcta (para verificar el ETL) y valores esperados de cada visual del dashboard |
| `salida/` | Tablas que el equipo exporta de Power BI (opcional) |

Las fuentes traen defectos a propósito (registros inválidos, duplicados, nombres de producto distintos, fechas con formatos mezclados,
nulos y días sin precio). Las fechas con barras son día/mes/año. Cada defecto está contado en `respuestas/defectos.csv`.
"""


def generar(params, salida):
    """Escribe en `salida` (la carpeta data/) las fuentes, el apoyo y la hoja de respuestas.

    Lanza ErrorDatos, sin escribir los archivos de datos, si alguna cifra queda fuera de su tolerancia."""
    sim = simular(params)
    malas = [c for c in sim["resumen"]["calibracion"] if not c[4]]
    if malas:
        raise ErrorDatos("cifras fuera de tolerancia: " + "; ".join(f"{n}: esperado {e}, obtenido {o}" for n, e, o, _, _ in malas))
    salida = Path(salida)
    (salida / "respuestas").mkdir(parents=True, exist_ok=True)
    for fu, (archivo, cab) in CABECERAS.items():
        _escribir(salida / archivo, cab, sim["filas"][fu])
    _escribir(salida / "apoyo-catalogo-productos.csv", ["producto", "categoria", "precio_lista", "pollos_equivalentes", "kg_pollo_vivo", "costo_otros", "alias"],
              [[p[0], p[1], m2(p[2]), m2(p[3]), m2(p[4]), m2(p[5]), "|".join(p[6])] for p in CATALOGO])
    ops = []
    for mes in sim["nombres"]:
        tot = sim["operativo"][mes]
        plan, alq, serv = round(tot * 0.62), round(tot * 0.17), round(tot * 0.13)
        ops.append([mes, plan, alq, serv, tot - plan - alq - serv, tot])
    _escribir(salida / "apoyo-costos-operativos.csv", ["mes", "planilla", "alquiler", "servicios", "otros", "total"], ops)
    res = salida / "respuestas"
    r = sim["resumen"]
    _escribir(res / "filas-por-fuente.csv", ["fuente", "filas_brutas", "filas_validas"], [[f, r["filas_brutas"][f], r["filas_validas"][f]] for f in sorted(r["filas_brutas"])])
    _escribir(res / "ventas-mes-canal.csv", ["mes", "canal", "lineas", "ventas", "comision"],
              [[m, c, v["lineas"], m2(v["ventas"]), m2(v["comision"])] for (m, c), v in sorted(sim["ventas"].items(), key=lambda kv: (kv[0][0], CANALES.index(kv[0][1])))])
    _escribir(res / "produccion-mes-turno.csv", ["mes", "turno", "preparados", "vendidos", "merma"],
              [[m, t, *x] for (m, t), x in sorted(sim["produccion"].items(), key=lambda kv: (kv[0][0], TURNOS.index(kv[0][1])))])
    _escribir(res / "precio-mes.csv", ["mes", "precio_medio", "dias_imputados"], [[m, m2(x[0] / x[1]), x[2]] for m, x in sorted(sim["precio_mes"].items())])
    _escribir(res / "defectos.csv", ["fuente", "defecto", "registros", "regla_sugerida"],
              [[f, d, c, REGLAS_FUENTE.get((f, d), REGLAS[d])] for (f, d), c in sorted(sim["defectos"].items())])
    _escribir(res / "margen-canal-producto.csv", ["mes", "canal", "producto", "lineas", "ventas", "comision", "costo_estimado", "margen_contribucion_pct"],
              [[m, c, pr, x[0], m2(x[1]), m2(x[2]), m2(x[3]), m2(_pct(x[1] - x[2] - x[3], x[1]))]
               for (m, c, pr), x in sorted(sim["por_producto"].items(), key=lambda kv: (kv[0][0], CANALES.index(kv[0][1]), [p[0] for p in CATALOGO].index(kv[0][2])))])
    _escribir(res / "produccion-dia-semana.csv", ["dia_semana", "preparados", "vendidos", "merma", "merma_pct"], sim["dia_semana"])
    _escribir(res / "precio-dia.csv", ["fecha", "precio_kg", "imputado"], sim["precio_dia"])
    _escribir(res / "pronostico-referencia.csv", ["fecha", "turno", "vendidos", "pronostico", "error_pct"], sim["pronostico"])
    _escribir(res / "kpi-esperados.csv", ["kpi", "mes", "valor", "unidad"], [list(x) for x in sim["kpi"]])
    (salida / "README.md").write_text(README.format(semilla=params["semilla"], inicio=params["periodo"]["inicio"], fin=params["periodo"]["fin"]), encoding="utf-8")
    return r


# ------------------------------------------------------------------ línea de comandos
def _mostrar(p):
    print(json.dumps(p, ensure_ascii=False, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("parametros", "generar", "verificar"):
        s = sub.add_parser(n)
        s.add_argument("--raiz", default=".")
        if n == "generar":
            s.add_argument("--confirmar", action="store_true", help="genera los archivos (el usuario ya confirmó los parámetros)")
        if n == "parametros":
            s.add_argument("--forzar", action="store_true", help="reemplaza data/parametros.json si ya existe")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "parametros":
            f = ruta_datos(a.raiz) / "parametros.json"
            if f.exists() and not a.forzar:
                print(f"{f} ya existe (usa --forzar para derivarlo de nuevo)")
                _mostrar(leer_parametros(a.raiz))
                return 0
            p = derivar_parametros(a.raiz)
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f)
            _mostrar(p)
            return 0
        if a.cmd == "generar":
            p = leer_parametros(a.raiz)
            if not a.confirmar:
                print("Parámetros que se usarían (confírmalos con el usuario y ejecuta de nuevo con --confirmar):")
                _mostrar(p)
                return 0
            r = generar(p, ruta_datos(a.raiz))
            print(f"Generados {sum(r['filas_brutas'].values())} registros en {ruta_datos(a.raiz)}")
            for n, e, o, tol, ok in r["calibracion"]:
                print(f"  {'ok ' if ok else 'MAL'} {n}: esperado {e}, obtenido {o}")
            return 0
        import etl_verificacion as V
        return V.main(["--raiz", a.raiz])
    except ErrorDatos as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ImportError:
        print("ERROR: falta _shared/etl_verificacion.py (lo entrega la skill 08-make-etl)", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
