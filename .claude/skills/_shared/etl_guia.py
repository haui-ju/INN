#!/usr/bin/env python3
"""Guía paso a paso del ETL a la medida del caso (materiales/guia-power-query.md de la corrida de 08-make-etl).

  python3 .claude/skills/_shared/etl_guia.py construir --run CORRIDA [--raiz .]

Escribe la guía que usa el equipo en Power BI: por cada fuente, qué trae, qué defectos tiene y cuántos, por qué se tratan, cómo
(con el código M propuesto) y cuántas filas deben quedar después de cada paso. Las cifras salen de la limpieza de referencia
(etl_referencia.py), que coincide con la hoja de respuestas de data/respuestas/, y las tablas, claves y relaciones salen de
modelo.json. El código M es una propuesta que el equipo prueba en Power BI. Solo biblioteca estándar.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import etl_referencia as ER  # noqa: E402
import projectcfg as P  # noqa: E402

FERIADOS = [("2025-08-30", "Santa Rosa de Lima"), ("2025-10-08", "Combate de Angamos"), ("2025-11-01", "Todos los Santos"),
            ("2025-12-08", "Inmaculada Concepción"), ("2025-12-25", "Navidad"), ("2026-01-01", "Año Nuevo"), ("2026-04-02", "Jueves Santo"),
            ("2026-04-03", "Viernes Santo"), ("2026-05-01", "Día del Trabajo"), ("2026-06-29", "San Pedro y San Pablo"),
            ("2026-07-28", "Fiestas Patrias"), ("2026-07-29", "Fiestas Patrias"), ("2026-08-30", "Santa Rosa de Lima"),
            ("2026-10-08", "Combate de Angamos")]
TIPO_CANAL = {"Salón": "Presencial", "Para llevar": "Presencial", "WhatsApp": "Delivery propio", "Rappi": "Aplicación", "PedidosYa": "Aplicación"}
COMISION = {"Salón": 0, "Para llevar": 0, "WhatsApp": 0, "Rappi": 30, "PedidosYa": 25}


def n(x):
    """Entero con espacios como separador de miles."""
    return f"{int(round(x)):,}".replace(",", " ")


def s(x, dec=2):
    """Soles con punto decimal y espacios como separador de miles."""
    return f"{x:,.{dec}f}".replace(",", " ")


def _modelo(raiz):
    cfg = P.load(raiz)
    e = cfg["pasos"]["07-make-data-model-kpi"]
    return json.loads((P.run_dir("07-make-data-model-kpi", e["run"], raiz) / "modelo.json").read_text(encoding="utf-8"))


def _muestra(ruta, k=3):
    with open(ruta, encoding="utf-8") as f:
        return "".join(next(f) for _ in range(k + 1)).rstrip("\n")


def _meta(texto):
    """(valor, comparador) de una meta como «98 % o más» o «3 % o menos»; (None, None) si está pendiente."""
    m = re.match(r"\s*([\d.,]+)\s*%?\s*(o más|o menos)?", str(texto or ""))
    if not m or "pendiente" in str(texto).lower():
        return None, None
    return float(m.group(1).replace(",", ".")), ("≥" if m.group(2) == "o más" else "≤" if m.group(2) == "o menos" else "=")


FUNCIONES = '''**Consulta `RutaDatos`** (parámetro de texto, en «Administrar parámetros»): la carpeta con los CSV, por ejemplo `C:\\datos\\` (con la barra final).

**Consulta `LeerCsv`** (función): lee un CSV como texto, sin que Power BI adivine los tipos.

```m
(archivo as text) as table =>
let
    Origen = Csv.Document(File.Contents(RutaDatos & archivo), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

**Consulta `FechaTexto`** (función): entiende `2025-08-01`, `01/08/2025` y cualquiera de los dos con hora (`01/08/2025 13:09`).

```m
(t as nullable text) as nullable date =>
let
    s = Text.Trim(Text.Start(t ?? "", 10))
in
    if s = "" then null
    else if Text.Contains(s, "/") then
        try Date.FromText(s, [Format = "dd/MM/yyyy", Culture = "es-PE"]) otherwise null
    else
        try Date.FromText(s, [Format = "yyyy-MM-dd", Culture = "en-US"]) otherwise null
```

**Consulta `NumTexto`** (función): convierte un texto con punto decimal en número, y el texto vacío en `null`.

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? "")
in
    if s = "" then null else try Number.FromText(s, "en-US") otherwise null
```

**Consulta `HoraTexto`** (función): devuelve la hora (0 a 23) de `11:04` o de `2025-08-01 12:08:00`.

```m
(t as nullable text) as nullable number =>
let
    s = Text.Trim(t ?? ""),
    h = if Text.Contains(s, " ") then Text.AfterDelimiter(s, " ", {0, RelativePosition.FromEnd}) else s
in
    if Text.Length(h) >= 4 and Text.Middle(h, 2, 1) = ":" then try Number.FromText(Text.Start(h, 2), "en-US") otherwise null else null
```

**Consulta `TurnoDeHora`** (función): el turno que corresponde a una hora, con los mismos límites que `dTurno`.

```m
(h as nullable number) as text =>
    if h = null then "Sin hora"
    else if h >= 11 and h < 15 then "Mañana"
    else if h >= 15 and h < 19 then "Tarde"
    else if h >= 19 and h < 23 then "Noche"
    else "Fuera de turno"
```
'''

CAJA = '''```m
let
    Origen = LeerCsv("fue-01-caja.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                precio = NumTexto(f[precio_unitario]),
                dscto = NumTexto(f[descuento]) ?? 0,
                invalido = (cant = null) or (cant <= 0) or (precio = null),
                h = HoraTexto(f[hora])
            in
                [fuente = "FUE-01", pedido = f[ticket_id], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = f[canal], producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else Number.Round(cant * precio - dscto, 2), comision = 0,
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```'''

RAPPI = '''```m
let
    Origen = LeerCsv("fue-02-rappi.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (monto_n = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha_hora])
            in
                [fuente = "FUE-02", pedido = f[pedido_id], fecha = FechaTexto(f[fecha_hora]), hora = h, turno = TurnoDeHora(h),
                 canal = "Rappi", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n,
                 comision = if invalido then 0 else (NumTexto(f[comision]) ?? 0),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```'''

PEDIDOSYA = '''```m
let
    Origen = LeerCsv("fue-03-pedidosya.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cant]),
                total = NumTexto(f[total]),
                pct = NumTexto(f[comision_pct]) ?? 0,
                invalido = (total = null) or (f[estado] = "CANCELADO"),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-03", pedido = f[nro_pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "PedidosYa", producto_fuente = f[item], cantidad = cant ?? 0,
                 monto = if invalido then 0 else total,
                 comision = if invalido then 0 else Number.Round(total * pct / 100, 2),
                 es_invalido = invalido, cliente_id = null]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, cliente_id = nullable text])
in
    Filas
```'''

WHATSAPP = '''```m
let
    Origen = LeerCsv("fue-04-whatsapp.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                cant = NumTexto(f[cantidad]),
                monto_n = NumTexto(f[monto]),
                invalido = (cant = null) or (cant <= 0) or (monto_n = null),
                h = HoraTexto(f[fecha])
            in
                [fuente = "FUE-04", pedido = f[pedido], fecha = FechaTexto(f[fecha]), hora = h, turno = TurnoDeHora(h),
                 canal = "WhatsApp", producto_fuente = f[producto], cantidad = cant ?? 0,
                 monto = if invalido then 0 else monto_n, comision = 0,
                 es_invalido = invalido, telefono = f[telefono]]),
        type table [fuente = text, pedido = text, fecha = nullable date, hora = nullable number, turno = text, canal = text,
                    producto_fuente = text, cantidad = number, monto = number, comision = number, es_invalido = logical, telefono = nullable text])
in
    Filas
```

Después, en una consulta nueva `Clientes`, crea un código por cada teléfono distinto, y en `WhatsApp` cambia el teléfono por ese código:

```m
// Consulta Clientes
let
    Distintos = Table.Distinct(Table.SelectColumns(WhatsApp, {"telefono"})),
    Indice = Table.AddIndexColumn(Distintos, "n", 1, 1, Int64.Type),
    Codigo = Table.AddColumn(Indice, "cliente_id", each "C-" & Text.PadStart(Text.From([n]), 4, "0"), type text)
in
    Codigo
```

```m
// Al final de la consulta WhatsApp: reemplaza telefono por cliente_id
    Unido = Table.NestedJoin(Filas, {"telefono"}, Clientes, {"telefono"}, "c", JoinKind.LeftOuter),
    Anonimo = Table.ExpandTableColumn(Unido, "c", {"cliente_id"}),
    Resultado = Table.RemoveColumns(Anonimo, {"telefono"})
```
(Como `Clientes` se construye a partir de `WhatsApp`, crea primero `WhatsApp` con el teléfono, luego `Clientes`, y duplica `WhatsApp` como `WhatsApp_anonimo` para añadir estos tres pasos. En `WhatsApp_anonimo` la columna `telefono` ya no existe y aparece `cliente_id`.)'''

ANEXO = '''```m
// Consulta Pedidos_bruto
let
    Union = Table.Combine({Caja, Rappi, PedidosYa, WhatsApp_anonimo})
in
    Union
```'''

HOMOLOGAR = '''```m
// Consulta Pedidos_homologado (usa la consulta Alias del PAS-02)
let
    Cruce = Table.NestedJoin(Pedidos_bruto, {"producto_fuente"}, Alias, {"nombre_fuente"}, "a", JoinKind.LeftOuter),
    Producto = Table.ExpandTableColumn(Cruce, "a", {"producto"})
in
    Producto
```'''

DUPLICADOS = '''```m
// Consulta Pedidos_marcado
let
    Clave = Table.AddColumn(Pedidos_homologado, "clave", each [pedido] & "|" & [producto], type text),
    Grupos = Table.Group(Clave, {"clave"}, {{"filas", each Table.AddIndexColumn(_, "ord", 0, 1, Int64.Type), type table}}),
    Planas = Table.ExpandTableColumn(Grupos, "filas", List.RemoveItems(Table.ColumnNames(Clave), {"clave"}) & {"ord"}),
    Duplicado = Table.AddColumn(Planas, "es_duplicado", each [ord] > 0, type logical),
    Valido = Table.AddColumn(Duplicado, "registro_valido", each if [es_duplicado] or [es_invalido] then 0 else 1, Int64.Type)
in
    Valido
```'''

PRECIO = '''```m
// Consulta PrecioDia (de ella sale fPrecioInsumo)
let
    Origen = LeerCsv("fue-06-precios-pollo.csv"),
    Publicado = Table.FromRecords(
        Table.TransformRows(Origen, (f) => [fecha = FechaTexto(f[fecha]), precio_kg = NumTexto(f[precio_kg])]),
        type table [fecha = date, precio_kg = nullable number]),
    Dias = Table.SelectColumns(dCalendario, {"fecha"}),
    Cruce = Table.NestedJoin(Dias, {"fecha"}, Publicado, {"fecha"}, "p", JoinKind.LeftOuter),
    Precio = Table.ExpandTableColumn(Cruce, "p", {"precio_kg"}),
    Orden = Table.Sort(Precio, {{"fecha", Order.Ascending}}),
    Marca = Table.AddColumn(Orden, "valor_imputado", each if [precio_kg] = null then 1 else 0, Int64.Type),
    Relleno = Table.FillDown(Marca, {"precio_kg"}),
    Tipos = Table.TransformColumnTypes(Relleno, {{"precio_kg", type number}})
in
    Tipos
```'''

MEDIDAS = '''```m
// Consulta fPedidos
let
    // 1. Catálogo (equivalentes, kilos de pollo y otros insumos) y precio del pollo del día
    ConCat = Table.NestedJoin(Pedidos_marcado, {"producto"}, Catalogo, {"producto"}, "c", JoinKind.LeftOuter),
    ExpCat = Table.ExpandTableColumn(ConCat, "c", {"pollos_equivalentes", "kg_pollo_vivo", "costo_otros"}, {"eq", "kg", "otros"}),
    ConPrecio = Table.NestedJoin(ExpCat, {"fecha"}, PrecioDia, {"fecha"}, "p", JoinKind.LeftOuter),
    ExpPrecio = Table.ExpandTableColumn(ConPrecio, "p", {"precio_kg"}),
    // 2. Mes de la venta y venta válida de cada mes (para repartir el costo operativo)
    Mes = Table.AddColumn(ExpPrecio, "mes", each Date.ToText([fecha], [Format = "yyyy-MM", Culture = "en-US"]), type text),
    Venta = Table.AddColumn(Mes, "venta_bruta", each [monto] * [registro_valido], type number),
    VentaMes = Table.Group(Venta, {"mes"}, {{"venta_mes", each List.Sum([venta_bruta]), type number}}),
    ConMes = Table.NestedJoin(Venta, {"mes"}, VentaMes, {"mes"}, "vm", JoinKind.LeftOuter),
    ExpMes = Table.ExpandTableColumn(ConMes, "vm", {"venta_mes"}),
    ConOper = Table.NestedJoin(ExpMes, {"mes"}, CostosOperativos, {"mes"}, "co", JoinKind.LeftOuter),
    ExpOper = Table.ExpandTableColumn(ConOper, "co", {"total"}, {"total_mes"}),
    // 3. Medidas por línea (0 si el registro no es válido)
    Comision = Table.AddColumn(ExpOper, "comision_v", each [comision] * [registro_valido], type number),
    Cantidad = Table.AddColumn(Comision, "cantidad_v", each [cantidad] * [registro_valido], type number),
    Equivalentes = Table.AddColumn(Cantidad, "pollos_equivalentes", each [cantidad] * [eq] * [registro_valido], type number),
    CostoEst = Table.AddColumn(Equivalentes, "costo_estimado", each [registro_valido] * [cantidad] * ([kg] * [precio_kg] + [otros]), type number),
    CostoOp = Table.AddColumn(CostoEst, "costo_operativo", each if [venta_mes] = 0 then 0 else [total_mes] * [venta_bruta] / [venta_mes], type number),
    Total = Table.AddColumn(CostoOp, "registro_total", each 1, Int64.Type),
    // 4. Claves hacia las dimensiones
    KFecha = Table.AddColumn(Total, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KProd = Table.NestedJoin(KFecha, {"producto"}, dProducto, {"producto"}, "d1", JoinKind.LeftOuter),
    KProd2 = Table.ExpandTableColumn(KProd, "d1", {"producto_key"}),
    KCanal = Table.NestedJoin(KProd2, {"canal"}, dCanal, {"canal"}, "d2", JoinKind.LeftOuter),
    KCanal2 = Table.ExpandTableColumn(KCanal, "d2", {"canal_key"}),
    KTurno = Table.NestedJoin(KCanal2, {"turno"}, dTurno, {"turno"}, "d3", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "d3", {"turno_key"}),
    // 5. Solo las columnas del modelo
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "producto_key", "canal_key", "turno_key", "cantidad_v", "venta_bruta", "comision_v",
                                        "costo_estimado", "costo_operativo", "pollos_equivalentes", "registro_valido", "registro_total"}),
    Nombres = Table.RenameColumns(Sel, {{"cantidad_v", "cantidad"}, {"comision_v", "comision"}})
in
    Nombres
```'''

PRODUCCION = '''```m
// Consulta fProduccion
let
    Origen = LeerCsv("fue-05-produccion.csv"),
    Filas = Table.FromRecords(
        Table.TransformRows(Origen, (f) =>
            let
                prep = NumTexto(f[pollos_preparados]),
                ven = NumTexto(f[pollos_vendidos]),
                mer = NumTexto(f[pollos_merma])
            in
                [fecha = FechaTexto(f[fecha]), turno = f[turno], pollos_preparados = prep, pollos_vendidos = ven, pollos_merma = mer,
                 es_invalido = (prep = null) or (ven = null) or (ven > prep)]),
        type table [fecha = nullable date, turno = text, pollos_preparados = nullable number, pollos_vendidos = nullable number,
                    pollos_merma = nullable number, es_invalido = logical]),
    SinCopias = Table.Distinct(Filas, {"fecha", "turno"}),
    Validas = Table.SelectRows(SinCopias, each not [es_invalido]),
    KFecha = Table.AddColumn(Validas, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),
    KTurno = Table.NestedJoin(KFecha, {"turno"}, dTurno, {"turno"}, "t", JoinKind.LeftOuter),
    KTurno2 = Table.ExpandTableColumn(KTurno, "t", {"turno_key"}),
    Sel = Table.SelectColumns(KTurno2, {"fecha_key", "turno_key", "pollos_preparados", "pollos_vendidos", "pollos_merma"})
in
    Sel
```'''


def construir(raiz=".", run=None, salida=None):
    raiz = Path(raiz)
    pc = ER.puntos_de_control(raiz)
    modelo = _modelo(raiz)
    data = raiz / "data"
    params = json.loads((data / "parametros.json").read_text(encoding="utf-8"))
    cat = ER.leer(data / "apoyo-catalogo-productos.csv")
    F, ped, tab = pc["fuentes"], pc["pedidos"], pc["tablas"]
    efe = pc["efecto_ventas"]
    L = []
    w = L.append

    w("# Guía paso a paso del ETL en Power BI")
    w("")
    w("> **Esta guía la ejecuta el equipo en Power BI Desktop.** No se ejecutó Power Query para escribirla: el código M es una propuesta que "
      "se prueba y se ajusta. Lo que importa es el **punto de control** que cierra cada paso (cuántas filas deben quedar): si tu número "
      "coincide, el paso salió bien; si no, la tabla «Si tu número no coincide» de la sección 10 te dice qué paso revisar.")
    w("")
    w(f"Los datos son **generados para el proyecto** (`modo_datos: generado`) y cubren de {params['periodo']['inicio']} a {params['periodo']['fin']} "
      f"({pc['periodo']['dias']} días, un local). Están en la carpeta `data/`. Las cifras de esta guía salen de la hoja de respuestas "
      "(`data/respuestas/`): si sigues los pasos, tus resultados deberían coincidir con ellas.")
    w("")

    w("## 0. Antes de empezar")
    w("")
    w("### Qué vas a construir")
    w("")
    w("Nueve tablas con la forma de `modelo.json` (2.4): cuatro de hechos y cinco dimensiones.")
    w("")
    w("| Tabla | Qué guarda | Filas que debe tener |")
    w("|---|---|---|")
    for h in modelo["hechos"]:
        w(f"| `{h['nombre']}` | {h['granularidad']} | {n(tab[h['nombre']]) if h['nombre'] in tab else '—'} |")
    for d in modelo["dimensiones"]:
        w(f"| `{d['nombre']}` | Atributos: {', '.join(d['atributos'])} | {n(tab[d['nombre']]) if d['nombre'] in tab else '—'} |")
    w("")
    w("### Los archivos de `data/`")
    w("")
    w("| Archivo | Qué es | Filas | Defectos que trae |")
    w("|---|---|---|---|")
    w(f"| `fue-01-caja.csv` | Ventas del salón y para llevar (una fila por línea de ticket) | {n(F['fue-01']['filas'])} | fechas, nombres de producto, duplicados, vacíos y registros inválidos |")
    w(f"| `fue-02-rappi.csv` | Reporte de Rappi, con la comisión de cada línea | {n(F['fue-02']['filas'])} | fechas, nombres de producto, duplicados, cancelados y filas sin monto |")
    w(f"| `fue-03-pedidosya.csv` | Reporte de PedidosYa, con **otros nombres de columna** y la comisión como porcentaje | {n(F['fue-03']['filas'])} | los mismos |")
    w(f"| `fue-04-whatsapp.csv` | Pedidos del delivery propio, con el teléfono del cliente | {n(F['fue-04']['filas'])} | los mismos y datos personales |")
    w(f"| `fue-05-produccion.csv` | Pollos preparados, vendidos y merma por día y turno | {n(F['fue-05']['filas'])} | fechas, un responsable vacío, jornadas repetidas y jornadas imposibles |")
    w(f"| `fue-06-precios-pollo.csv` | Precio diario del kilo de pollo vivo | {n(F['fue-06']['filas'])} | fechas y {F['fue-06']['dias_sin_precio']} días sin precio |")
    w(f"| `apoyo-catalogo-productos.csv` | Lista de precios y receta de cada producto, con los nombres que usan las fuentes | {len(cat)} | ninguno (es la referencia para homologar) |")
    w("| `apoyo-costos-operativos.csv` | Costo operativo de cada mes (planilla, alquiler, servicios y otros) | 15 | ninguno |")
    w("")
    w("### Tres cosas de configuración que evitan la mitad de los errores")
    w("")
    w("1. **Codificación UTF-8** (`Encoding = 65001` en el código M): si no, «Salón» y «Mañana» salen con símbolos raros.")
    w("2. **El punto es el separador decimal** en los archivos (`62.00`). Tu Windows puede estar en español con coma decimal: por eso el código lee los "
      "números con `Number.FromText(texto, \"en-US\")`. **No dejes que Power BI «detecte el tipo»** al importar: puede leer `62.00` como texto o como 6200.")
    w("3. **Las fechas con barras son día/mes/año** (`03/08/2025` es el 3 de agosto). Si Power BI las lee como mes/día, las ventas de agosto "
      "aparecen en marzo. El código fija el formato.")
    w("")
    w("### Cómo llevar tu propia evidencia")
    w("")
    w("En cada paso, anota **cuántas filas tenía la tabla antes y después**. Al final hay una tabla para copiar esas cifras: son la evidencia "
      "(`evidencia.json`) con la que se redactan la sección 3.1 y el anexo A. Si algo no coincide, no sigas: corrige y vuelve a contar.")
    w("")

    w("## 1. Pasos del ETL")
    w("")
    w("| Código | Paso | Resultado esperado |")
    w("|---|---|---|")
    pasos = [
        ("PAS-01", "Crear el parámetro `RutaDatos` y las funciones auxiliares", "Seis consultas de ayuda, sin tablas cargadas"),
        ("PAS-02", "Importar el catálogo, los alias y los costos operativos", f"`Catalogo` ({len(cat)} filas), `Alias` ({len(cat) * 4} filas), `CostosOperativos` (15 filas)"),
        ("PAS-03", "Importar y limpiar la caja (FUE-01)", f"{n(F['fue-01']['filas'])} filas en el esquema común"),
        ("PAS-04", "Importar y limpiar Rappi (FUE-02)", f"{n(F['fue-02']['filas'])} filas en el esquema común"),
        ("PAS-05", "Importar y limpiar PedidosYa (FUE-03)", f"{n(F['fue-03']['filas'])} filas en el esquema común"),
        ("PAS-06", "Importar WhatsApp (FUE-04) y anonimizar el teléfono", f"{n(F['fue-04']['filas'])} filas y {n(pc['telefonos_distintos'])} clientes con código"),
        ("PAS-07", "Anexar las cuatro fuentes", f"`Pedidos_bruto` con {n(ped['filas'])} filas"),
        ("PAS-08", "Homologar los nombres de producto", "Ninguna fila sin producto del catálogo"),
        ("PAS-09", "Marcar duplicados y registros válidos", f"{n(ped['duplicados'])} duplicados, {n(ped['invalidos'])} inválidos y {n(ped['validas'])} válidos"),
        ("PAS-10", "Calendario, dimensiones y claves", "`dCalendario`, `dProducto`, `dCanal`, `dTurno` y `dKpi`"),
        ("PAS-11", "Precio diario del pollo e imputación", f"{pc['periodo']['dias']} días, {pc['precio']['imputados']} imputados"),
        ("PAS-12", "Calcular las medidas de `fPedidos`", f"`fPedidos` con {n(tab['fPedidos'])} filas y los totales de la sección 7"),
        ("PAS-13", "Construir `fProduccion`", f"{n(tab['fProduccion'])} filas"),
        ("PAS-14", "Construir `fMetaKpi`", f"{tab['fMetaKpi']} filas"),
        ("PAS-15", "Cargar el modelo y crear las relaciones", "Nueve relaciones, de varios a uno"),
        ("PAS-16", "Verificar contra la hoja de respuestas", "Los totales coinciden"),
    ]
    for c, t, r in pasos:
        w(f"| {c} | {t} | {r} |")
    w("")
    w("| Código | Regla de calidad | Defecto que trata | Paso |")
    w("|---|---|---|---|")
    reglas = [("REG-01", "Estandarizar todas las fechas a un solo formato", "`formato_fecha`", "PAS-01, 03 a 06, 11, 13"),
              ("REG-02", "Homologar el nombre de cada producto contra el catálogo", "`nombre_producto`", "PAS-08"),
              ("REG-03", "Marcar y no contar las copias duplicadas", "`duplicado`", "PAS-09, 13"),
              ("REG-04", "Marcar y no contar los registros inválidos (sin cantidad o monto, o cancelados)", "`registro_invalido`", "PAS-03 a 06, 09, 13"),
              ("REG-05", "Completar los vacíos que se pueden deducir", "`nulo`", "PAS-03, 13"),
              ("REG-06", "Imputar el precio de los días sin precio y marcarlos", "`dia_sin_precio`", "PAS-11"),
              ("REG-07", "Reemplazar el teléfono del cliente por un código", "datos personales", "PAS-06")]
    for r in reglas:
        w("| " + " | ".join(r) + " |")
    w("")

    # ---------------------------------------------------------------- PAS-01
    w("## 2. Preparación (PAS-01 y PAS-02)")
    w("")
    w("### PAS-01. El parámetro y las funciones auxiliares")
    w("")
    w("En Power BI Desktop: **Transformar datos** (abre el Editor de Power Query). Crea cada elemento con **Nueva consulta ▸ Consulta en blanco** y "
      "pega el código en el **Editor avanzado**. Estas consultas **no se cargan al modelo**: desmarca «Habilitar carga» (clic derecho sobre la consulta).")
    w("")
    w(FUNCIONES)
    w("**Punto de control:** seis consultas de ayuda (`RutaDatos`, `LeerCsv`, `FechaTexto`, `NumTexto`, `HoraTexto`, `TurnoDeHora`). "
      "Prueba `FechaTexto(\"03/08/2025 13:09\")` y `FechaTexto(\"2025-08-03\")`: ambas deben dar el **3 de agosto de 2025**.")
    w("")
    w("### PAS-02. Catálogo, alias y costos operativos")
    w("")
    w("El **catálogo** es la lista de precios y recetas del dueño. Es la referencia para homologar nombres y para calcular costos. "
      "Cada producto trae sus **alias**: los nombres con que lo escriben las fuentes.")
    w("")
    w("```text")
    w(_muestra(data / "apoyo-catalogo-productos.csv", 3))
    w("```")
    w("")
    w("```m")
    w("// Consulta Catalogo")
    w("let")
    w('    Enc = LeerCsv("apoyo-catalogo-productos.csv"),')
    w("    Tipos = Table.TransformColumnTypes(Enc, {{\"precio_lista\", type number}, {\"pollos_equivalentes\", type number},")
    w("                                            {\"kg_pollo_vivo\", type number}, {\"costo_otros\", type number}}, \"en-US\")")
    w("in")
    w("    Tipos")
    w("```")
    w("")
    w("Los alias se separan con `|`. Para homologar necesitas **una fila por cada nombre posible** (el alias y el nombre oficial):")
    w("")
    w("```m")
    w("// Consulta Alias")
    w("let")
    w('    ConAlias = Table.AddColumn(Catalogo, "nombre_fuente", each Text.Split([alias], "|") & {[producto]}, type list),')
    w("    Expandida = Table.ExpandListColumn(ConAlias, \"nombre_fuente\"),")
    w('    Alias = Table.SelectColumns(Expandida, {"nombre_fuente", "producto"})')
    w("in")
    w("    Alias")
    w("```")
    w("")
    w("```m")
    w("// Consulta CostosOperativos (el costo del local de cada mes)")
    w("let")
    w('    Enc = LeerCsv("apoyo-costos-operativos.csv"),')
    w("    Tipos = Table.TransformColumnTypes(Enc, {{\"planilla\", type number}, {\"alquiler\", type number}, {\"servicios\", type number},")
    w("                                            {\"otros\", type number}, {\"total\", type number}}, \"en-US\")")
    w("in")
    w("    Tipos")
    w("```")
    w("")
    w(f"**Punto de control:** `Catalogo` {len(cat)} filas; `Alias` {len(cat) * 4} filas ({len(cat)} nombres oficiales y {len(cat) * 3} alias); "
      f"`CostosOperativos` 15 filas (de 2025-08 a 2026-10). El total de `CostosOperativos` suma **S/ {s(pc['totales']['costo_operativo'], 0)}**.")
    w("")

    # ---------------------------------------------------------------- Fuentes
    w("## 3. Las cuatro fuentes de ventas (PAS-03 a PAS-06)")
    w("")
    w("Las cuatro fuentes dicen casi lo mismo (quién compró qué, cuándo, por cuánto) con **columnas distintas**. El primer objetivo es llevarlas todas al "
      "mismo **esquema común**:")
    w("")
    w("| Columna común | Qué es |")
    w("|---|---|")
    for a, b in [("fuente", "FUE-01 a FUE-04"), ("pedido", "Identificador del ticket o pedido"), ("fecha", "Fecha ya convertida (REG-01)"),
                 ("hora y turno", "La hora de la venta y su turno (Mañana 11–15, Tarde 15–19, Noche 19–23)"), ("canal", "Salón, Para llevar, WhatsApp, Rappi o PedidosYa"),
                 ("producto_fuente", "El nombre tal como lo escribe la fuente (se homologa después)"), ("cantidad", "Unidades de la línea"),
                 ("monto", "Venta de la línea en soles (0 si la fila es inválida)"), ("comision", "Comisión de la aplicación (0 en los canales propios)"),
                 ("es_invalido", "`true` si la fila no sirve (REG-04)"), ("cliente_id", "Solo en WhatsApp: un código en lugar del teléfono (REG-07)")]:
        w(f"| `{a}` | {b} |")
    w("")
    w("En las cuatro consultas se hace lo mismo: se lee todo como texto, se convierte cada campo con las funciones auxiliares y se marca la fila inválida. "
      "**Nada se borra todavía**: así puedes contar.")
    w("")

    def fuente(titulo, cod, archivo, c, codigo, extra):
        w(f"### {titulo}")
        w("")
        w("```text")
        w(_muestra(data / archivo, 3))
        w("```")
        w("")
        w("| Defecto | Cuántas filas | Por qué importa | Cómo se trata |")
        w("|---|---|---|---|")
        for fila in extra(c):
            w("| " + " | ".join(fila) + " |")
        w("")
        w(codigo)
        w("")
        return c

    def comunes(c, fecha_col, con_nulos=False, cancel=False):
        filas = [
            ("Fechas en el otro formato (REG-01)", f"{n(c['formato_fecha_archivo'])}",
             "Un día/mes/año leído como mes/día mueve ventas de mes", "`FechaTexto` entiende los dos formatos"),
            ("Nombres de producto distintos (REG-02)", f"{n(c['nombre_producto_archivo'])}",
             "Un mismo producto aparecería con varios nombres y su margen quedaría repartido", "Se homologan en el PAS-08"),
            ("Copias duplicadas (REG-03)", f"{n(c['duplicados'])}", "Cada copia suma otra vez la venta", "Se marcan en el PAS-09"),
            ("Registros inválidos (REG-04)", f"{n(c['invalidos'])}", "Sin cantidad o monto no hay venta que contar", "`es_invalido = true` y monto 0"),
        ]
        if con_nulos:
            filas.append(("Vacíos (REG-05)", f"{n(c['nulo_archivo'])}", "Un turno vacío rompe el análisis por turno; un descuento vacío es 0",
                          "El turno se deduce de la hora; el descuento vacío vale 0"))
        if cancel:
            filas.append(("Pedidos cancelados (parte de REG-04)", f"{n(c['cancelados'])}", f"Suman S/ {s(c['monto_cancelados'])} que no se cobraron",
                          "Cuentan como inválidos"))
        return filas

    c = F["fue-01"]
    fuente("PAS-03. Caja (FUE-01)", "FUE-01", "fue-01-caja.csv", c, CAJA, lambda c: comunes(c, "fecha", con_nulos=True))
    w(f"**Punto de control:** la consulta `Caja` tiene **{n(c['filas'])} filas**; si filtras `es_invalido = true` y `fecha` vacía, no debe quedar ninguna fecha vacía. "
      f"Cuenta las filas con barras en la fecha: **{n(c['formato_fecha_archivo'])}** (incluye las copias duplicadas).")
    w("")
    c = F["fue-02"]
    fuente("PAS-04. Rappi (FUE-02)", "FUE-02", "fue-02-rappi.csv", c, RAPPI, lambda c: comunes(c, "fecha_hora", cancel=True))
    w(f"**Punto de control:** `Rappi` tiene **{n(c['filas'])} filas**. La comisión ya viene en cada fila (30 % del monto).")
    w("")
    c = F["fue-03"]
    fuente("PAS-05. PedidosYa (FUE-03)", "FUE-03", "fue-03-pedidosya.csv", c, PEDIDOSYA, lambda c: comunes(c, "fecha", cancel=True))
    w("Aquí las columnas se llaman distinto (`nro_pedido`, `item`, `cant`, `total`) y **la comisión no viene en soles sino como porcentaje** (`comision_pct`, 25): "
      "se calcula como `total × comision_pct / 100`, redondeada a dos decimales.")
    w("")
    w(f"**Punto de control:** `PedidosYa` tiene **{n(c['filas'])} filas**. Las fechas de este archivo vienen **con barras** (día/mes/año): las "
      f"**{n(c['formato_fecha_archivo'])}** que vienen con guiones son las que están en el «otro» formato.")
    w("")
    c = F["fue-04"]
    fuente("PAS-06. WhatsApp (FUE-04) y datos personales", "FUE-04", "fue-04-whatsapp.csv", c, WHATSAPP, lambda c: comunes(c, "fecha"))
    w("**REG-07, el teléfono:** el número identifica a una persona (Ley 29733, de Protección de Datos Personales). El análisis no lo necesita: "
      "solo necesita saber **si es el mismo cliente**. Por eso se reemplaza por un código (`C-0001`, `C-0002`…) antes de cargar el modelo. "
      "Nunca cargues el teléfono al modelo ni al informe.")
    w("")
    w(f"**Punto de control:** `WhatsApp_anonimo` tiene **{n(c['filas'])} filas** y **{n(pc['telefonos_distintos'])} clientes distintos** (`Clientes`); "
      "la columna `telefono` ya no existe.")
    w("")

    # ---------------------------------------------------------------- Anexar
    w("## 4. Unir y marcar (PAS-07 a PAS-09)")
    w("")
    w("### PAS-07. Anexar las cuatro fuentes")
    w("")
    w(ANEXO)
    w("")
    suma = " + ".join(n(F[f]["filas"]) for f in ("fue-01", "fue-02", "fue-03", "fue-04"))
    w(f"**Punto de control:** `Pedidos_bruto` tiene **{n(ped['filas'])} filas** ({suma}). Este número es el **total de registros leídos** "
      f"y es el denominador de KPI-01 (calidad de datos).")
    w("")
    w("### PAS-08. Homologar los nombres de producto (REG-02)")
    w("")
    w("Las fuentes escriben el mismo producto de varias maneras. Mira los nombres distintos de `producto_fuente` en `Pedidos_bruto` "
      "(Vista de columnas: «Distribución de la columna»): verás **unos 32 nombres** para **8 productos**. Se unen contra `Alias`:")
    w("")
    w(HOMOLOGAR)
    w("")
    w("Ejemplo: `POLLO ENTERO`, `Pollo entero` y `Pollo a la brasa entero` pasan todos a **Pollo entero a la brasa**.")
    w("")
    w(f"**Punto de control:** la tabla sigue con **{n(ped['filas'])} filas** y **ninguna** con `producto` vacío "
      f"(filtra `producto = null`: deben ser {ped['sin_homologar']}). Si hay filas vacías, hay un nombre que no está en `Alias`: revisa tildes y espacios. "
      f"Debes ver exactamente **{len(cat)}** productos distintos.")
    w("")
    w("### PAS-09. Marcar duplicados y registros válidos (REG-03 y REG-04)")
    w("")
    w("Una **copia duplicada** es una fila idéntica a otra (mismo pedido y mismo producto) que se coló dos veces, por ejemplo cuando el reporte de una "
      "aplicación se descargó dos veces. Si no se trata, la venta se cuenta doble. Para no perder la cuenta de lo que llegó, **no se borra**: se marca. "
      "Una fila es **válida** si no es copia y no es inválida.")
    w("")
    w(DUPLICADOS)
    w("")
    w("| Resultado | Filas | Cómo contarlo |")
    w("|---|---|---|")
    w(f"| Filas leídas | {n(ped['filas'])} | todas las filas de la tabla |")
    w(f"| Copias duplicadas | {n(ped['duplicados'])} | `es_duplicado = true` |")
    w(f"| Quedan sin copias | {n(ped['tras_duplicados'])} | `es_duplicado = false` |")
    w(f"| Inválidas entre las que quedan | {n(ped['invalidos'])} | `es_duplicado = false` y `es_invalido = true` |")
    w(f"| **Válidas** | **{n(ped['validas'])}** | `registro_valido = 1` |")
    w("")
    w(f"**Por qué importa:** si no quitas las copias, las ventas suben **S/ {s(efe['duplicados'])}** de más; si cuentas los cancelados de las aplicaciones, "
      f"suben **S/ {s(efe['cancelados'])}**. KPI-01 (calidad de datos) = filas válidas ÷ filas leídas = **{s(100 * ped['validas'] / ped['filas'])} %**, "
      "por encima de su meta de 98 %.")
    w("")
    w("> Las cifras de «copias» de la hoja `defectos.csv` cuentan cada copia **una vez**, y los demás defectos sobre las filas **sin copias**; "
      "por eso algunos conteos que haces sobre el archivo tal cual llega salen un poco mayores (las copias traen los mismos defectos). Esta guía te da "
      "las dos cifras cuando difieren.")
    w("")

    # ---------------------------------------------------------------- Dimensiones
    w("## 5. Dimensiones y claves (PAS-10)")
    w("")
    w("Una **dimensión** es una lista corta de «cosas» por las que se analiza (días, productos, canales, turnos, indicadores). "
      "Cada una lleva una **clave** (`*_key`) y los hechos guardan esa clave para unirse a ella.")
    w("")
    w("### `dCalendario`: un día por fila")
    w("")
    w(f"Todos los días del periodo, **también los que no tuvieron ventas** ({pc['periodo']['dias']} días). El calendario es la columna vertebral del tiempo: "
      "sin él no se puede hacer la imputación del precio ni comparar meses.")
    w("")
    w("```m")
    w("// Consulta Feriados (lista de referencia: ajústala con el calendario oficial)")
    w("{ " + ", ".join(f"#date({a[:4]}, {int(a[5:7])}, {int(a[8:])})" for a, _ in FERIADOS) + " }")
    w("```")
    w("")
    w("```m")
    w("// Consulta dCalendario")
    w("let")
    ini, fin = params["periodo"]["inicio"], params["periodo"]["fin"]
    w(f"    Inicio = #date({ini[:4]}, {int(ini[5:7])}, {int(ini[8:])}),")
    w(f"    Fin = #date({fin[:4]}, {int(fin[5:7])}, {int(fin[8:])}),")
    w("    Dias = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),")
    w('    Tabla = Table.FromList(Dias, Splitter.SplitByNothing(), {"fecha"}, null, ExtraValues.Error),')
    w('    Tipada = Table.TransformColumnTypes(Tabla, {{"fecha", type date}}),')
    w('    Clave = Table.AddColumn(Tipada, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + Date.Day([fecha]), Int64.Type),')
    w('    Anio = Table.AddColumn(Clave, "anio", each Date.Year([fecha]), Int64.Type),')
    w('    Mes = Table.AddColumn(Anio, "mes", each Date.Month([fecha]), Int64.Type),')
    w('    NombreMes = Table.AddColumn(Mes, "nombre_mes", each {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"}{Date.Month([fecha]) - 1}, type text),')
    w('    DiaSemana = Table.AddColumn(NombreMes, "dia_semana", each {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"}{Date.DayOfWeek([fecha], Day.Monday)}, type text),')
    w('    Feriado = Table.AddColumn(DiaSemana, "es_feriado", each List.Contains(Feriados, [fecha]), type logical)')
    w("in")
    w("    Feriado")
    w("```")
    w("")
    w(f"**Punto de control:** **{pc['periodo']['dias']} filas**, de {ini} a {fin}. `fecha_key` del 1 de agosto de 2025 = `20250801`.")
    w("")
    w("### `dProducto`, `dCanal`, `dTurno` y `dKpi`")
    w("")
    w("```m")
    w("// Consulta dProducto")
    w("let")
    w('    Cols = Table.SelectColumns(Catalogo, {"producto", "categoria"}),')
    w('    Clave = Table.AddIndexColumn(Cols, "producto_key", 1, 1, Int64.Type)')
    w("in")
    w("    Clave")
    w("```")
    w("")
    w("```m")
    w("// Consulta dCanal")
    w("let")
    w("    Datos = #table(type table [canal = text, tipo_canal = text, comision_pct = number],")
    w("        {" + ", ".join(f'{{"{c}", "{TIPO_CANAL[c]}", {COMISION[c]}}}' for c in ("Salón", "Para llevar", "WhatsApp", "Rappi", "PedidosYa")) + "}),")
    w('    Clave = Table.AddIndexColumn(Datos, "canal_key", 1, 1, Int64.Type)')
    w("in")
    w("    Clave")
    w("```")
    w("")
    w("```m")
    w("// Consulta dTurno")
    w("let")
    w("    Datos = #table(type table [turno = text, hora_inicio = time, hora_fin = time],")
    w('        {{"Mañana", #time(11, 0, 0), #time(15, 0, 0)}, {"Tarde", #time(15, 0, 0), #time(19, 0, 0)}, {"Noche", #time(19, 0, 0), #time(23, 0, 0)}}),')
    w('    Clave = Table.AddIndexColumn(Datos, "turno_key", 1, 1, Int64.Type)')
    w("in")
    w("    Clave")
    w("```")
    w("")
    filas_kpi = []
    for k in modelo["kpis"]:
        v, comp = _meta(k["meta"])
        filas_kpi.append(f'{{"{k["nombre"]}", "{k["objetivo"]}", {"true" if v is not None else "false"}, "{k["frecuencia"]}"}}')
    w("```m")
    w("// Consulta dKpi: los indicadores de 2.5")
    w("let")
    w("    Datos = #table(type table [kpi = text, objetivo = text, tiene_meta = logical, frecuencia = text],")
    w("        {" + ",\n         ".join(filas_kpi) + "}),")
    w('    Clave = Table.AddIndexColumn(Datos, "kpi_key", 1, 1, Int64.Type)')
    w("in")
    w("    Clave")
    w("```")
    w("")
    w(f"**Punto de control:** `dProducto` **{len(cat)}** filas; `dCanal` **5**; `dTurno` **3**; `dKpi` **7**. "
      "En `dKpi`, `tiene_meta` es `false` para los KPI cuya meta sigue pendiente en 2.5.")
    w("")

    # ---------------------------------------------------------------- Precio
    w("## 6. El precio del pollo vivo (PAS-11)")
    w("")
    w(f"El boletín de precios trae **{F['fue-06']['filas']} filas para {pc['periodo']['dias']} días**: faltan **{pc['precio']['imputados']}** (fines de semana y feriados en que no se publicó). "
      "Pero el costo del pollo se calcula **día por día**: si un día no tiene precio, el costo de ese día saldría **0** y el margen se vería inflado.")
    w("")
    w("La regla (REG-06): **usar el último precio publicado** y marcar el día como imputado (`valor_imputado = 1`) para que se pueda medir cuánto del dato es estimado.")
    w("")
    w("```text")
    w(_muestra(data / "fue-06-precios-pollo.csv", 3))
    w("```")
    w("")
    w(PRECIO)
    w("")
    w("**Consulta `fPrecioInsumo`:** copia `PrecioDia`, agrega `fecha_key` (igual que en `dCalendario`) y deja `fecha_key`, `precio_kg`, `valor_imputado`.")
    w("")
    w(f"**Punto de control:** `PrecioDia` tiene **{pc['periodo']['dias']} filas**; `valor_imputado = 1` en **{pc['precio']['imputados']}**; el precio del "
      f"**1 de julio de 2026 es S/ {pc['precio']['precio_1_julio']:.2f}** y el del **14 de julio, S/ {pc['precio']['precio_14_julio']:.2f}** (el salto del que habla el informe).")
    w("")

    # ---------------------------------------------------------------- Medidas
    w("## 7. Las medidas de `fPedidos` (PAS-12)")
    w("")
    w("Hasta aquí cada fila dice qué pasó. Ahora se le agrega **cuánto vale**: la venta, la comisión, el costo del pollo y del local. Todas se multiplican por "
      "`registro_valido` (1 o 0), de modo que las filas duplicadas o inválidas **siguen en la tabla pero no suman**.")
    w("")
    w("| Columna | Cómo se calcula | De dónde salen los datos |")
    w("|---|---|---|")
    w("| `venta_bruta` | `monto × registro_valido` | caja: `cantidad × precio_unitario − descuento`; apps y WhatsApp: el monto de la fuente |")
    w("| `comision` | `comision × registro_valido` | Rappi: viene en soles; PedidosYa: `total × comision_pct / 100`; caja y WhatsApp: 0 |")
    w("| `pollos_equivalentes` | `cantidad × pollos_equivalentes del producto × registro_valido` | `apoyo-catalogo-productos.csv` |")
    w("| `costo_estimado` | `cantidad × (kg_pollo_vivo × precio del pollo del día + costo_otros) × registro_valido` | catálogo + `PrecioDia` |")
    w("| `costo_operativo` | `costo del mes × venta_bruta de la línea ÷ venta_bruta del mes` | `apoyo-costos-operativos.csv` |")
    w("| `registro_valido` / `registro_total` | 1 si es válida, 0 si no / 1 en toda fila leída | marcas del PAS-09 |")
    w("")
    w("Ejemplo: un **Pollo entero** vendido el 14 de julio con el pollo vivo a S/ 6.90 cuesta `1.90 kg × 6.90 + 9.00 = S/ 22.11`; "
      f"con el pollo a S/ 6.10 habría costado S/ {1.90 * 6.10 + 9.0:.2f}. Esa diferencia es la que erosiona el margen en los últimos meses.")
    w("")
    w(MEDIDAS)
    w("")
    t = pc["totales"]
    w(f"**Punto de control:** `fPedidos` tiene **{n(tab['fPedidos'])} filas** y `SUM(registro_valido)` = **{n(t['lineas'])}**. Los totales de las columnas son:")
    w("")
    w("| Columna | Total esperado |")
    w("|---|---|")
    w(f"| `venta_bruta` | S/ {s(t['ventas'])} |")
    w(f"| `comision` | S/ {s(t['comision'])} |")
    w(f"| `costo_estimado` | S/ {s(t['costo_estimado'])} |")
    w(f"| `costo_operativo` | S/ {s(t['costo_operativo'])} |")
    w(f"| Margen neto del periodo | {s(100 * (t['ventas'] - t['comision'] - t['costo_estimado'] - t['costo_operativo']) / t['ventas'])} % |")
    w("")

    # ---------------------------------------------------------------- Producción
    w("## 8. Producción y metas (PAS-13 y PAS-14)")
    w("")
    w("### PAS-13. `fProduccion`")
    w("")
    w(f"La cocina anota por cada día y turno cuántos pollos preparó, cuántos vendió y cuántos sobraron (merma). Defectos: "
      f"**{F['fue-05']['duplicados']}** jornadas repetidas, **{F['fue-05']['invalidos']}** jornadas imposibles (vendidos mayores que preparados), "
      f"**{F['fue-05']['formato_fecha']}** fechas en el otro formato y **{F['fue-05']['nulo']}** responsables vacíos (no afectan a ningún KPI; se pueden dejar como «Sin dato»).")
    w("")
    w("```text")
    w(_muestra(data / "fue-05-produccion.csv", 3))
    w("```")
    w("")
    w(PRODUCCION)
    w("")
    pr = F["fue-05"]
    w(f"**Punto de control:** {n(pr['filas'])} filas leídas → {n(pr['tras_duplicados'])} sin repetidas → **{n(pr['validas'])}** válidas. "
      f"Debería haber {pc['periodo']['dias']} días × 3 turnos = {pc['periodo']['dias'] * 3} jornadas; faltan {pc['periodo']['dias'] * 3 - pr['validas']} "
      "porque las jornadas imposibles se excluyen.")
    w("")
    w("### PAS-14. `fMetaKpi`")
    w("")
    w("Una fila por indicador y mes, con su **meta** (de 2.5). La columna `valor_real` queda vacía en el ETL: se calcula con las medidas del dashboard "
      "(en la guía del dashboard) y se compara con la meta.")
    w("")
    metas = ", ".join(f"{{{i + 1}, {_meta(k['meta'])[0] if _meta(k['meta'])[0] is not None else 'null'}}}" for i, k in enumerate(modelo["kpis"]))
    w("```m")
    w("// Consulta fMetaKpi")
    w("let")
    w("    Meses = List.Transform({0..14}, each Date.AddMonths(#date(2025, 8, 1), _)),")
    w(f"    Metas = #table(type table [kpi_key = Int64.Type, meta = nullable number], {{{metas}}}),")
    w('    Cruce = Table.AddColumn(Metas, "fecha", each Meses, type list),')
    w('    Expandida = Table.ExpandListColumn(Cruce, "fecha"),')
    w('    Clave = Table.AddColumn(Expandida, "fecha_key", each Date.Year([fecha]) * 10000 + Date.Month([fecha]) * 100 + 1, Int64.Type),')
    w('    Real = Table.AddColumn(Clave, "valor_real", each null, type nullable number),')
    w('    Sel = Table.SelectColumns(Real, {"kpi_key", "fecha_key", "meta", "valor_real"})')
    w("in")
    w("    Sel")
    w("```")
    w("")
    w("| KPI | Meta de 2.5 |")
    w("|---|---|")
    for k in modelo["kpis"]:
        w(f"| {k['codigo']} {k['nombre']} | {k['meta']} |")
    w("")
    w(f"**Punto de control:** **{tab['fMetaKpi']} filas** (7 indicadores × 15 meses). KPI-02 y KPI-06 quedan con meta vacía (pendiente).")
    w("")

    # ---------------------------------------------------------------- Cargar y relaciones
    w("## 9. Cargar y relacionar (PAS-15)")
    w("")
    w("Cierra el editor con **Cerrar y aplicar**. Solo se cargan las nueve tablas del modelo; las demás consultas quedan como ayuda. "
      "Luego, en la **Vista de modelo**, crea estas relaciones (de varios a uno, un solo sentido de filtro):")
    w("")
    w("| Código | Desde (varios) | Hacia (uno) | Campo | Cardinalidad | Filtro |")
    w("|---|---|---|---|---|---|")
    for r in modelo["relaciones"]:
        w(f"| {r['codigo']} | `{r['desde']}` | `{r['hacia']}` | `{r['campos']}` | {r['cardinalidad']} | {r['filtro']} |")
    w("")
    w("Marca `dCalendario` como **tabla de fechas** (Herramientas de tabla ▸ Marcar como tabla de fechas ▸ columna `fecha`) y ordena `nombre_mes` por `mes` "
      "y `dia_semana` por su número para que los gráficos salgan en orden.")
    w("")
    w("**Punto de control:** la vista de modelo muestra **nueve relaciones** y ninguna advertencia de relación ambigua o activa a medias.")
    w("")

    # ---------------------------------------------------------------- Verificación
    w("## 10. Verificar contra la hoja de respuestas (PAS-16)")
    w("")
    w("Crea estas medidas en una tabla vacía (Entrar datos ▸ tabla `_Medidas`) y arma una tabla con **mes** (`dCalendario[anio]`, `dCalendario[mes]`) y las medidas:")
    w("")
    w("```dax")
    w("Ventas = SUM(fPedidos[venta_bruta])")
    w("Comisión = SUM(fPedidos[comision])")
    w("Costo estimado = SUM(fPedidos[costo_estimado])")
    w("Costo operativo = SUM(fPedidos[costo_operativo])")
    w("Margen neto % = DIVIDE([Ventas] - [Comisión] - [Costo estimado] - [Costo operativo], [Ventas])")
    w("Filas leídas = SUM(fPedidos[registro_total])")
    w("Filas válidas = SUM(fPedidos[registro_valido])")
    w("```")
    w("")
    w("Tus valores deben coincidir con estos (tolerancia: un centavo por redondeo):")
    w("")
    kpi3 = {}
    with open(data / "respuestas" / "kpi-esperados.csv", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if fila["kpi"] == "KPI-03":
                kpi3[fila["mes"]] = fila["valor"]
    w("| Mes | Ventas | Comisión | Costo estimado | Costo operativo | Margen neto |")
    w("|---|---|---|---|---|---|")
    for m, x in pc["meses"].items():
        w(f"| {m} | {s(x['ventas'])} | {s(x['comision'])} | {s(x['costo_estimado'])} | {s(x['costo_operativo'], 0)} | {kpi3[m]} % |")
    w("")
    w("Por canal (todo el periodo):")
    w("")
    w("| Canal | Líneas válidas | Ventas | Comisión |")
    w("|---|---|---|---|")
    for cnl, x in pc["canales"].items():
        w(f"| {cnl} | {n(x['lineas'])} | {s(x['ventas'])} | {s(x['comision'])} |")
    w("")
    w("La hoja completa (por mes y canal) está en `data/respuestas/ventas-mes-canal.csv`. Si prefieres que lo compare un programa, exporta tus tablas a "
      "`data/salida/<tabla>.csv` (`fPedidos`, `fProduccion`, `fPrecioInsumo`, `dCalendario`, `dCanal`, `dTurno`) y ejecuta "
      "`python3 .claude/skills/_shared/datagen.py verificar`: te dice la tabla, el mes y la diferencia.")
    w("")
    w("### Si tu número no coincide")
    w("")
    w("| Lo que ves | Causa más probable |")
    w("|---|---|")
    w(f"| Ventas mayores en ≈ S/ {s(efe['duplicados'], 0)} | No marcaste las copias duplicadas (PAS-09) |")
    w(f"| Ventas mayores en ≈ S/ {s(efe['cancelados'], 0)} | Contaste los pedidos cancelados de Rappi y PedidosYa |")
    w("| Un mes con ventas de otro mes | Las fechas con barras se leyeron como mes/día (usa `FechaTexto`) |")
    w("| Margen de contribución demasiado alto en un producto | Productos sin homologar: el costo no se pudo calcular |")
    w("| Margen neto más alto en los días de julio | Días sin precio sin imputar (el costo del pollo sale 0) |")
    w("| Números con millones de pesos de más o de menos | El punto decimal se leyó como separador de miles (usa `en-US`) |")
    w("| `fPedidos` con más o menos filas que las leídas | Borraste filas en vez de marcarlas, o dejaste una consulta sin anexar |")
    w("| Una columna con `Error` | Un nombre de producto sin alias, o un texto con espacios (revisa el PAS-08) |")
    w("")

    # ---------------------------------------------------------------- Evidencia
    w("## 11. Lo que debes anotar y traer")
    w("")
    w("Copia tus cifras en esta tabla (las esperadas son las de la hoja de respuestas). Con ella se redacta la sección 3.1 y el anexo A:")
    w("")
    w("| Regla | Defecto | Filas antes | Filas después | Lo esperado |")
    w("|---|---|---|---|---|")
    w(f"| REG-01 | Fechas en otro formato | — | — | {n(sum(F[f]['formato_fecha_archivo'] for f in ('fue-01', 'fue-02', 'fue-03', 'fue-04')) + F['fue-05']['formato_fecha'] + F['fue-06']['formato_fecha'])} fechas convertidas, 0 sin entender |")
    w(f"| REG-02 | Nombres de producto | {n(ped['filas'])} | {n(ped['filas'])} | {len(cat)} productos, 0 sin catálogo |")
    w(f"| REG-03 | Copias duplicadas | {n(ped['filas'])} | {n(ped['tras_duplicados'])} | {n(ped['duplicados'])} copias |")
    w(f"| REG-04 | Registros inválidos | {n(ped['tras_duplicados'])} | {n(ped['validas'])} | {n(ped['invalidos'])} inválidos |")
    w(f"| REG-05 | Vacíos | — | — | turno deducido de la hora; descuento vacío = 0 |")
    w(f"| REG-06 | Días sin precio | {n(F['fue-06']['filas'])} | {pc['periodo']['dias']} | {pc['precio']['imputados']} días imputados |")
    w(f"| REG-07 | Teléfonos | {n(F['fue-04']['filas'])} | {n(F['fue-04']['filas'])} | {n(pc['telefonos_distintos'])} clientes con código |")
    w("")
    w("Y las filas de cada tabla cargada:")
    w("")
    w("| Tabla | Filas esperadas |")
    w("|---|---|")
    for k, v in tab.items():
        w(f"| `{k}` | {n(v)} |")
    w("")
    w("Trae además: **tus scripts** (las consultas de Power Query, para el anexo B), **capturas** del editor con los conteos y los **totales** de la sección 10. "
      "Con eso se redacta el ETL; **nada de esta guía se da por hecho hasta que lo traigas**.")
    w("")

    # ---------------------------------------------------------------- Diccionario
    w("## Apéndice. Diccionario de datos")
    w("")
    w("### Tablas del modelo y origen de cada campo")
    w("")
    w("| Tabla | Campo | Tipo | Origen |")
    w("|---|---|---|---|")
    origen = {
        "fPedidos": {"fecha_key": ("entero", "FUE-01 a FUE-04: fecha"), "producto_key": ("entero", "Catálogo: producto homologado"),
                     "canal_key": ("entero", "FUE-01 a FUE-04: canal"), "turno_key": ("entero", "FUE-01 a FUE-04: hora → turno"),
                     "cantidad": ("número", "FUE-01 a FUE-04: cantidad"), "venta_bruta": ("número", "Cálculo: monto de la línea"),
                     "comision": ("número", "FUE-02: comision; FUE-03: Cálculo total × comision_pct / 100"),
                     "costo_estimado": ("número", "Cálculo: apoyo-catalogo-productos y FUE-06"),
                     "costo_operativo": ("número", "Cálculo: apoyo-costos-operativos"),
                     "pollos_equivalentes": ("número", "Cálculo: apoyo-catalogo-productos"),
                     "registro_valido": ("entero", "Cálculo: marcas de duplicado e inválido"), "registro_total": ("entero", "Cálculo: 1 por fila leída")},
        "fProduccion": {"fecha_key": ("entero", "FUE-05: fecha"), "turno_key": ("entero", "FUE-05: turno"),
                        "pollos_preparados": ("número", "FUE-05: pollos_preparados"), "pollos_vendidos": ("número", "FUE-05: pollos_vendidos"),
                        "pollos_merma": ("número", "FUE-05: pollos_merma")},
        "fPrecioInsumo": {"fecha_key": ("entero", "dCalendario: fecha"), "precio_kg": ("número", "FUE-06: precio_kg (imputado si falta)"),
                          "valor_imputado": ("entero", "Cálculo: 1 si el día no tenía precio")},
        "fMetaKpi": {"kpi_key": ("entero", "dKpi"), "fecha_key": ("entero", "Cálculo: primer día de cada mes"), "meta": ("número", "Cálculo: metas de 2.5"),
                     "valor_real": ("número", "Cálculo: medidas del dashboard")},
        "dCalendario": {"fecha": ("fecha", "Cálculo: lista de días"), "anio": ("entero", "Cálculo: fecha"), "mes": ("entero", "Cálculo: fecha"),
                        "nombre_mes": ("texto", "Cálculo: fecha"), "dia_semana": ("texto", "Cálculo: fecha"), "es_feriado": ("lógico", "Cálculo: lista de feriados")},
        "dProducto": {"producto": ("texto", "apoyo-catalogo-productos: producto"), "categoria": ("texto", "apoyo-catalogo-productos: categoria")},
        "dCanal": {"canal": ("texto", "Cálculo: lista de canales"), "tipo_canal": ("texto", "Cálculo: lista de canales"), "comision_pct": ("número", "Cálculo: 30 Rappi, 25 PedidosYa")},
        "dTurno": {"turno": ("texto", "Cálculo: lista de turnos"), "hora_inicio": ("hora", "Cálculo: lista de turnos"), "hora_fin": ("hora", "Cálculo: lista de turnos")},
        "dKpi": {"kpi": ("texto", "Cálculo: 2.5"), "objetivo": ("texto", "Cálculo: 2.5"), "tiene_meta": ("lógico", "Cálculo: meta de 2.5"), "frecuencia": ("texto", "Cálculo: 2.5")},
    }
    for h in modelo["hechos"]:
        for c in h["claves"] + [m["nombre"] for m in h["medidas"]]:
            tipo, org = origen.get(h["nombre"], {}).get(c, ("", "por definir"))
            w(f"| `{h['nombre']}` | `{c}` | {tipo} | {org} |")
    for d in modelo["dimensiones"]:
        w(f"| `{d['nombre']}` | `{d['clave']}` | entero | Cálculo: número de fila |")
        for c in d["atributos"]:
            tipo, org = origen.get(d["nombre"], {}).get(c, ("", "por definir"))
            w(f"| `{d['nombre']}` | `{c}` | {tipo} | {org} |")
    w("")
    w("### Campos de las fuentes")
    w("")
    for archivo in ("fue-01-caja.csv", "fue-02-rappi.csv", "fue-03-pedidosya.csv", "fue-04-whatsapp.csv", "fue-05-produccion.csv", "fue-06-precios-pollo.csv"):
        with open(data / archivo, encoding="utf-8") as f:
            cab = f.readline().strip().split(",")
        w(f"- **`{archivo}`:** " + ", ".join(f"`{c}`" for c in cab))
    w("")
    w("Todas las columnas llegan como **texto**; la conversión a número, fecha y lógico (`true` o `false`) la hace el código de esta guía.")
    w("")

    texto = "\n".join(L)
    if salida is None:
        salida = P.run_dir("08-make-etl", run, raiz) / "materiales" / "guia-power-query.md"
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto + "\n", encoding="utf-8")
    return salida


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("construir")
    c.add_argument("--run", required=True)
    c.add_argument("--raiz", default=".")
    a = ap.parse_args(argv)
    print(construir(a.raiz, a.run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
